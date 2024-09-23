import json
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from matchmaking.asgi import application
from .models import Match
from .enums import *
from .consumers import match_played

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
