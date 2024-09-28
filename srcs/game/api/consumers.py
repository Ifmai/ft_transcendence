import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameState:
    def __init__(self, capacity):
        self.capacity = capacity
        self.paddles = self._initialize_paddles(capacity)
        self.ball = self._initialize_ball()

    def _initialize_paddles(self, capacity):
        paddles = {
            'left': {'position': 0, 'velocity': 0},
            'right': {'position': 0, 'velocity': 0}
        }
        if capacity == 4:
            paddles.update({
                'up': {'position': 0, 'velocity': 0},
                'down': {'position': 0, 'velocity': 0}
            })
        return paddles

    def _initialize_ball(self):
        return {'positionX': 0, 'positionY': 0, 'velocityX': 0.5, 'velocityY': 0.5}

    def update_ball_position(self):
        # Update the ball's position
        self.ball['positionX'] += self.ball['velocityX']
        self.ball['positionY'] += self.ball['velocityY']

    def check_paddle_collision(self):
        # Handle paddle collision detection logic
        pass

    def check_wall_collision(self):
        # Handle ball collision with walls logic
        pass

    def reset_game(self):
        # Reset ball and paddles to initial positions
        self.__init__(self.capacity)

class PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
		try:
			room_id = self.scope['url_route']['kwargs'].get('room_id')
			self.capacity =  self.scope['url_route']['kwargs'].get('capacity')
			self.match_id = self.scope['url_route']['kwargs'].get('match_id')
		except KeyError as e:
			print(f"Error getting scope: {e}")

		await self.send(text_data=json.dumps({'message': 'Connected', 'status': 200, 'room_id': room_id}))
