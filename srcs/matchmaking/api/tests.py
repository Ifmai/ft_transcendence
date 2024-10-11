import json
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from matchmaking.asgi import application
from .models import Match, Tournament
from .enums import *
from .consumers import match_played
import uuid
from .consumers import game_rooms
from asgiref.sync import sync_to_async

User = get_user_model()

class MatchMakerConsumerTest(TransactionTestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.match = Match.objects.create(id=1, state=State.PLAYED.value)
        self.unplayed_match = Match.objects.create(id=2, state=State.UNPLAYED.value)

    async def test_websocket_connect_with_valid_token(self):
        communicator = WebsocketCommunicator(
            application, f"/ws/matchmaking/10/2/?token={self.token}"
        )

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()

        self.assertEqual(response, {'message': 'Connected', 'status': 200, 'match_id': 2})

        self.assertEqual(self.user.username, 'testuser')

        await communicator.disconnect()
    async def test_websocket_connect_with_invalid_token(self):
        # Test with a match_id in the URL but an invalid JWT token in the query string
        communicator = WebsocketCommunicator(
            application, "/ws/matchmaking/10/5/?token=invalidtoken"
        )

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()

        self.assertEqual(response, {'message': 'User not authenticated', 'status': 403})

        # Ensure the user is not set (since the token is invalid)
        self.assertIsNone(communicator.scope.get('user'))

        await communicator.disconnect()
    async def test_match_played_returns_true_for_played_match(self):
        result = await match_played(self.match.id)
        self.assertTrue(result, "match_played should return True for a played match.")

    async def test_match_played_returns_false_for_unplayed_match(self):
        result = await match_played(self.unplayed_match.id)
        self.assertFalse(result, "match_played should return False for an unplayed match.")

    async def test_match_played_returns_false_for_non_existent_match(self):
        non_existent_id = 9999
        result = await match_played(non_existent_id)
        self.assertFalse(result, "match_played should return False for a non-existent match.")

    async def test_websocket_connect_to_played_match(self):
        communicator = WebsocketCommunicator(
            application, f"/ws/matchmaking/10/1/?token={self.token}"  # match_id 1 is already played
    )

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()
        self.assertEqual(response, {'message': "Match's Already Been Played", 'status': 400})

        await communicator.disconnect()

    async def test_join_full_room(self):
    # Create a room with 2 players
        global game_rooms
        room_id = str(uuid.uuid4())
        game_rooms[room_id] = {
        "players": [{self.user.id: 'channel_1'}, {self.user.id + 1: 'channel_2'}],
        "match_id": self.unplayed_match.id,
        "capacity": 2
    }

        communicator = WebsocketCommunicator(
            application, f"/ws/matchmaking/2/{self.unplayed_match.id}/?token={self.token}"
    )

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()
        self.assertEqual(response, {'message': 'No room found', 'status': 400})

        await communicator.disconnect()

    async def test_game_start_after_capacity_reached(self):
        communicator1 = WebsocketCommunicator(
            application, f"/ws/matchmaking/2/{self.unplayed_match.id}/?token={self.token}"
        )
        connected1, subprotocol1 = await communicator1.connect()
        self.assertTrue(connected1)

        second_user = await sync_to_async(User.objects.create_user)(
            username='seconduser', password='testpassword')
        refresh = RefreshToken.for_user(second_user)
        second_token = str(refresh.access_token)

        communicator2 = WebsocketCommunicator(
            application, f"/ws/matchmaking/2/{self.unplayed_match.id}/?token={second_token}"
            )
        connected2, subprotocol2 = await communicator2.connect()
        self.assertTrue(connected2)

        response1 = await communicator1.receive_json_from()
        response2 = await communicator2.receive_json_from()

        self.assertEqual(response1['message'], 'Connected')
        self.assertEqual(response2['message'], 'Connected')

        self.assertNotIn(self.unplayed_match.id, game_rooms)

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_tournament_deleted_on_creator_disconnect(self):
        communicator = WebsocketCommunicator(
            application, f"/ws/matchmaking/10/2/?token={self.token}"
        )

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Simulate disconnect
        await communicator.disconnect()

        # Check if the tournament is deleted
        tournament_exists = await Tournament.objects.filter(id=self.tournament.id).exists()
        self.assertFalse(tournament_exists)
