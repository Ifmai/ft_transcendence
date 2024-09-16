
import json
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from api.consumers import MatchMakerConsumer
from matchmaking.asgi import application

class MatchMakerConsumerTest(TransactionTestCase):
    async def test_websocket_connect(self):
        # Setup a WebsocketCommunicator that will connect to our consumer
        communicator = WebsocketCommunicator(application, "/ws/matchmaking/")

        connected, subprotocol = await communicator.connect()

        self.assertTrue(connected)

        response = await communicator.receive_json_from()

        self.assertEqual(response, {'message': 'Connected', 'status': 200})

        await communicator.disconnect()
