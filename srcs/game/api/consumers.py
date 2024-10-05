import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Profil

rooms = dict()

PADDLE_TEMPLATE = {
    'left': {'speed': 30, 'positionX': 0, 'positionY': 0, 'sizeX': 40, 'sizeY': 200, 'eliminated': False},
    'right': {'speed': 30, 'positionX': 0, 'positionY': 0, 'sizeX': 40, 'sizeY': 200, 'eliminated': False},
    'up': {'speed': 30, 'positionX': 0, 'positionY': 0, 'sizeX': 200, 'sizeY': 40, 'eliminated': False},
    'down': {'speed': 30, 'positionX': 0, 'positionY': 0, 'sizeX': 200, 'sizeY': 40, 'eliminated': False}
}

class GameState:
    def __init__(self, capacity):
        self.capacity = capacity
        self.paddles = None
        self.ball = None

    def _initialize_paddles(self, capacity, width, height):
        paddles = {
            'left': {'positionY':  height / 2 - 50, 'velocity': "15"},
            'right': {'positionY': height / 2 - 50, 'velocity': 15}
        }
        if capacity == 4:
            paddles.update({
                'up': {'positionY': height / 2 - 50, 'velocity': 15},
                'down': {'positionY': height / 2 - 50, 'velocity': 15}
            })
        return paddles

    def _initialize_ball(self, width, height):
        return {
            'positionX': width / 2,
            'positionY': height / 2,
            'velocityX': 0.5,
            'velocityY': 0.5
        }

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
			self.game_state = GameState(self.capacity)
			self.user = self.scope['user']
		except KeyError as e:
			print(f"Error getting scope: {e}")

		player_db = None
		if (self.user):
			try:
				player_db = await database_sync_to_async(Profil.objects.get)(user_id=self.user.id)
			except Profil.DoesNotExist:
				print("User not found")

		await self.channel_layer.group_add(
			room_id,
			self.channel_name
		)

		if room_id not in rooms:
			rooms[room_id] = {}

		print("Before: ", rooms[room_id])
		# rooms[room_id].append(self.channel_name)
		await self.assign_paddle(room_id, player_db)
		print("After: ", rooms[room_id])

		await self.send_initial_state()

		# if len(rooms[room_id]) == self.game_state.capacity:
		# 	await self.start_game(room_id)

	async def assign_paddle(self, room_id, player_db):
		"""Assign a paddle to the player based on available slots."""
		paddle_positions = ['left', 'right', 'up', 'down']
		for position in paddle_positions[:self.capacity]:
			if position not in rooms[room_id]:
				rooms[room_id][position] = {
					'player': self.channel_name,
					'user_id': self.user.id,
					'info': PADDLE_TEMPLATE[position].copy(),
					'alias': player_db.alias_name,
					'avatar': player_db.photo
				}
				await self.send(str(paddle_positions.index(position) + 1))
				break

	async def send_initial_state(self):
		# Send initial game state to the clients
		await self.send(text_data=json.dumps(self.game_state.__dict__))

	async def broadcast_game_state(self, room_id):
		"""Broadcast the game state to all players in the room."""
		await self.channel_layer.group_send(
			room_id,
			{
				'type': 'pong_message',
				'message': self.game_state.__dict__
			}
		)
	async def disconnect(self, close_code):
		room_id = self.scope['url_route']['kwargs'].get('room_id')
		if room_id in rooms:
			for position in rooms[room_id]:
				if (rooms[room_id][position]['player'] == self.channel_name):
					rooms[room_id].pop(position)
					break
			if len(rooms[room_id]) == 0:
				del rooms[room_id]
		await self.channel_layer.group_discard(
			room_id,
			self.channel_name
		)
	async def pong_message(self, event):
		# Send updated game state to the clients
		await self.send(text_data=json.dumps(event['message']))

	async def receive(self, text_data):
		data = json.loads(text_data)
		if data['type'] == 'initialize':
			width = data['width']
			height = data['height']
			self.game_state.ball = self.game_state._initialize_ball(width, height)
			self.game_state.paddles = self.game_state._initialize_paddles(self.capacity, width, height)
			await self.send_initial_state()
		elif data['type'] == 'keyPress':
			print(data)
