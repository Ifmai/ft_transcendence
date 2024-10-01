from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from game.asgi import application
from .models import Match
from .enums import State

User = get_user_model()

class PongConsumerTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.match = Match.objects.create(id=1, state=State.PLAYED.value)
        self.unplayed_match = Match.objects.create(id=2, state=State.UNPLAYED.value)

    async def test_websocket_connect_with_valid_token(self):
        communicator = WebsocketCommunicator(
            application, f"/ws/pong/game_room_42/2/5/?token={self.token}"
        )

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()

        self.assertEqual(self.user.username, 'testuser')
