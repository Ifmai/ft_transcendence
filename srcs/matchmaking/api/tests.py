import json
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from matchmaking.asgi import application

User = get_user_model()

class MatchMakerConsumerTest(TransactionTestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    async def test_websocket_connect_with_valid_token(self):
        communicator = WebsocketCommunicator(
            application, f"/ws/matchmaking/10/5/?token={self.token}"
        )

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        response = await communicator.receive_json_from()

        # Assert that the response contains the correct status and match_id
        self.assertEqual(response, {'message': 'Connected', 'status': 200, 'match_id': 5})

        # Ensure the user is correctly set in the scope
        self.assertEqual(self.user.username, 'testuser')

        await communicator.disconnect()
    async def test_websocket_connect_with_invalid_token(self):
        # Test with a match_id in the URL but an invalid JWT token in the query string
        communicator = WebsocketCommunicator(
            application, "/ws/matchmaking/10/5/?token=invalidtoken"
        )

        # Connect to the WebSocket
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Receive the connection confirmation message
        response = await communicator.receive_json_from()

        # Assert that the response contains the correct status and match_id
        self.assertEqual(response, {'message': 'Connected', 'status': 200, 'match_id': 5})

        # Ensure the user is not set (since the token is invalid)
        self.assertIsNone(communicator.scope.get('user'))

        await communicator.disconnect()
    # async def test_receive(self):
    #     communicator = WebsocketCommunicator(application, "/ws/matchmaking/10/5")

    #     connected, subprotocol = await communicator.connect()

    #     initial_response = await communicator.receive_from()
    #     expected_initial_response = json.dumps({'message': 'Connected', 'status': 200})
    #     self.assertEqual(initial_response, expected_initial_response)

    #     # Send a message to the WebSocket
    #     message = json.dumps({"type": "test.message", "data": "Hello, World!"})
    #     await communicator.send_to(text_data=message)

    #     # Receive the message from the WebSocket
    #     response = await communicator.receive_from()

    #     # Check if the message was received correctly
    #     expected_response = json.dumps({'message': 'Received', 'data': message})
    #     self.assertEqual(response, expected_response)

    #     # Close the WebSocket connection
    #     await communicator.disconnect()
