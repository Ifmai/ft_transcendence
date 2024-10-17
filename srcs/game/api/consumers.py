import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Profil, Match, PlayerMatch
import asyncio
import time
from .enums import State

rooms = dict()

PADDLE_TEMPLATE = {
	'left': {'velocity': 20, 'positionX': 0, 'positionY': 0, 'sizeX': 20, 'sizeY': 150, 'eliminated': False, 'score': 0},
	'right': {'velocity': 20, 'positionX': 0, 'positionY': 0, 'sizeX': 20, 'sizeY': 150, 'eliminated': False, 'score': 0},
}

class GameState:
	def __init__(self, capacity, match_id, channel_layer, room_id):
		self.capacity = capacity
		self.match_id = match_id
		self.channel_layer = channel_layer
		self.room_id = room_id
		self.paddles = None
		self.ball = None

	def _initialize_paddles(self, width, height):
		paddles = {
			'left' : rooms[self.room_id]['left']['info'],
			'right': rooms[self.room_id]['right']['info']
		}
		return paddles

	def _initialize_ball(self, width, height):
		return {
			'positionX': width / 2,
			'positionY': height / 2,
			'velocityX': 10,
			'velocityY': 10,
			'radius': 20
		}

	def update_ball_position(self):
		# Update the ball's position
		self.ball['positionX'] += self.ball['velocityX']
		self.ball['positionY'] += self.ball['velocityY']

	def check_paddle_collision(self, width):
		for position, paddle in self.paddles.items():
			paddle_x = 0 if position == 'left' else width - paddle['sizeX']
			paddle_y = paddle['positionY']

			paddle_center_x = paddle_x + (paddle['sizeX'] / 2)
			paddle_center_y = paddle_y + (paddle['sizeY'] / 2)

			dx = abs(self.ball['positionX'] - paddle_center_x)
			dy = abs(self.ball['positionY'] - paddle_center_y)

			half_paddle_width = paddle['sizeX'] / 2
			half_paddle_height = paddle['sizeY'] / 2

			if dx <= (self.ball['radius'] + half_paddle_width) and dy <= (self.ball['radius'] + half_paddle_height):
				self.ball['velocityX'] *= -1
				if self.ball['positionX'] < paddle_center_x:
					self.ball['positionX'] = paddle_center_x - (self.ball['radius'] + half_paddle_width)
				else:
					self.ball['positionX'] = paddle_center_x + (self.ball['radius'] + half_paddle_width)

	def check_wall_collision(self, width, height):
		# Handle ball collision with walls logic
		if (self.ball['positionY'] + self.ball['radius'] > height or
				self.ball['positionY'] - self.ball['radius'] <= 0):
			self.ball['velocityY'] *= -1

	def get_match(self, match_id):
		if not match_id:
			new_match = Match.objects.create(state=State.PLAYED.value)
			self.match_id = new_match.id
			return new_match
		match = Match.objects.get(id=match_id)
		match.state = State.PLAYED.value
		match.save()
		return match

	@database_sync_to_async
	def set_db_two_players(self, room_id, match_id):
		player_left = rooms[room_id]['left']
		player_right = rooms[room_id]['right']
		try:
			match = self.get_match(match_id)
			player_left_db = Profil.objects.get(id=player_left['user_id'])
			player_right_db = Profil.objects.get(id=player_right['user_id'])

			player_match_left, _ = PlayerMatch.objects.get_or_create(
			match_id=match.id,
			player_id=player_left_db.id
			)
			player_match_left.score = player_left['info']['score']
			player_match_left.won = player_left['info']['score'] == 3
			player_match_left.save()

			player_match_right, _ = PlayerMatch.objects.get_or_create(
			match_id=match.id,
			player_id=player_right_db.id
			)
			player_match_right.score = player_right['info']['score']
			player_match_right.won = player_right['info']['score'] == 3
			player_match_right.save()

			if player_left['info']['score'] == 3:
				player_left_db.wins += 1
				player_right_db.losses += 1
				winner = player_left_db.user.username
			else:
				player_left_db.losses += 1
				player_right_db.wins += 1
				winner = player_right_db.user.username

			player_right_db.save()
			player_left_db.save()

			return f"{winner} won"

		except Profil.DoesNotExist as e:
			print(f"Error: {e}", flush=True)
			return "Error retrieving profiles"
		except Exception as e:
			print(f"Unexpected error: {e}", flush=True)
			return "Unexpected error"

	async def reset_game(self, width, height, room_id):
		# Reset ball and paddles to initial positions
		self.ball['positionX'] = width / 2
		self.ball['positionY'] = height / 2
		self.paddles['left']['positionY'] = height / 2 - self.paddles['left']['sizeY'] / 2
		self.paddles['right']['positionY'] = height / 2 - self.paddles['right']['sizeY'] / 2
		rooms[room_id]['left']['info']['positionY'] = self.paddles['left']['positionY']
		rooms[room_id]['right']['info']['positionY'] = self.paddles['right']['positionY']

		time.sleep(1)

	async def update_score(self, width, height, room_id):
		game_reset = False
		match_end = False
		if self.paddles['left']['score'] != 3 and self.paddles['right']['score'] != 3:
			if self.ball['positionX'] <= -self.ball['radius']:
				self.paddles['right']['score'] += 1
				rooms[room_id]['right']['info']['score'] += 1
				await self.reset_game(width, height, room_id)
				game_reset = True
			elif self.ball['positionX'] >= self.ball['radius'] + width:
				self.paddles['left']['score'] += 1
				rooms[room_id]['left']['info']['score'] += 1
				await self.reset_game(width, height, room_id)
				game_reset = True
		else:
			"Temporary announce the winner"
			await self.reset_game(width, height, room_id)
			if self.paddles['left']['score'] == 3:
				result = await self.set_db_two_players(room_id, self.match_id)
				await self.announce_winner(result)
			elif self.paddles['right']['score'] == 3:
				result = await self.set_db_two_players(room_id, self.match_id)
				await self.announce_winner(result)
			game_reset = True
			match_end = True

		return game_reset, match_end

	async def announce_winner(self, result):
		"""Send the winner announcement to all players in the room."""
		message = {
			'type': 'pong.message',
			'message': result
		}
		await self.channel_layer.group_send(
			self.room_id,
			{
				'type': 'pong_message',
				'message': {'won': message}
			}
		)
	async def announce_game_finish(self):
		message = {
			'type': 'pong.message',
			'message': 'match ended'
		}
		await self.channel_layer.group_send(
			self.room_id,
			{
				'type': 'pong_message',
				'message': {'end': message}
			}
		)

class PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
		try:
			self.room_id = self.scope['url_route']['kwargs'].get('room_id')
			self.capacity =  self.scope['url_route']['kwargs'].get('capacity')
			self.match_id = self.scope['url_route']['kwargs'].get('match_id')
			self.game_state = GameState(self.capacity, self.match_id, self.channel_layer, self.room_id)
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
			self.room_id,
			self.channel_name
		)

		if self.room_id not in rooms:
			rooms[self.room_id] = {}

		await self.assign_paddle(player_db)

		await self.send_initial_state()


	async def assign_paddle(self, player_db):
		"""Assign a paddle to the player based on available slots."""
		paddle_positions = ['left', 'right']
		for position in paddle_positions[:self.capacity]:
			if position not in rooms[self.room_id]:
				rooms[self.room_id][position] = {
					'player': self.channel_name,
					'user_id': self.user.id,
					'info': PADDLE_TEMPLATE[position].copy(),
					'alias': player_db.alias_name,
					'avatar': player_db.photo.url
				}
				await self.send(str(paddle_positions.index(position) + 1))
				break

	async def send_initial_state(self):
		# Send initial game state to the clients
		await self.send(text_data=json.dumps({"message": f"{self.game_state.__dict__}", "type": "initialize"}))

	async def broadcast_paddle_state(self,position):
		"""Broadcast the game state to all players in the room."""
		paddle_state = {position: self.game_state.paddles[position]}
		await self.channel_layer.group_send(
			self.room_id,
			{
				'type': 'pong_message',
				'message': {'paddles': paddle_state}
			}
		)

	async def broadcast_ball_state(self):
		"""Broadcast the current ball state to all players in the room."""
		ball_state = self.game_state.ball
		await self.channel_layer.group_send(
			self.room_id,
			{
				'type': 'pong_message',
				'message': {'ball': ball_state}
			}
		)

	async def broadcast_score(self):
		"""Broadcast the current score to all players in the room."""
		scores = {position: rooms[self.room_id][position]['info']['score'] for position in rooms[self.room_id]}
		await self.channel_layer.group_send(
		self.room_id,
		{
			'type': 'pong_message',
			'message': {'scores': scores}
		}
	)

	async def disconnect(self, close_code):
		if self.room_id in rooms:
			for position in rooms[self.room_id]:
				if (rooms[self.room_id][position]['player'] == self.channel_name):
					rooms[self.room_id].pop(position)
					break
			if len(rooms[self.room_id]) == 0:
				del rooms[self.room_id]
		await self.channel_layer.group_discard(
			self.room_id,
			self.channel_name
		)

	async def pong_message(self, event):
		# Send updated game state to the clients
		await self.send(text_data=json.dumps(event['message']))

	async def start_game(self, height, width):
		# Start the game loop
		await self.send(text_data=json.dumps({"message": f"Game starting in room: {self.room_id}"})) # random message will be modified
		while True:
			self.game_state.update_ball_position()
			self.game_state.check_wall_collision(width, height)
			self.game_state.check_paddle_collision(width)
			game_reset , match_end = await self.game_state.update_score(width, height, self.room_id)
			await self.broadcast_ball_state()
			await self.broadcast_score()
			if (game_reset):
				await self.broadcast_paddle_state('left')
				await self.broadcast_paddle_state('right')
			if match_end:
				self.game_state.announce_game_finish()
				break
			await asyncio.sleep(0.03)


	async def receive(self, text_data):
		data = json.loads(text_data)
		if data['type'] == 'initialize':
			self.width = data['width']
			self.height = data['height']
			self.game_state.ball = self.game_state._initialize_ball(self.width, self.height)
			self.game_state.paddles = self.game_state._initialize_paddles(self.width, self.height)
			await self.send_initial_state()

			if len(rooms[self.room_id]) == self.game_state.capacity:
				asyncio.create_task(self.start_game(self.height, self.width))

		elif data['type'] == 'keyPress':
			await self.handle_key_press(data)

	async def handle_key_press(self, data):
		"""Handle paddle movement based on key presses."""
		paddles = self.game_state.paddles

		 # Handle paddle movement based on key presses
		for position, paddle_data in rooms[self.room_id].items():
			if paddle_data['player'] == self.channel_name:
				if data['keyCode'] == 38:
					if paddles[position]['positionY'] > 0:
						paddles[position]['positionY'] -= float(paddles[position]['velocity'])
				elif data['keyCode'] == 40:
					if paddles[position]['positionY'] + (PADDLE_TEMPLATE[position]['sizeY'] / 2) <= self.height:
						paddles[position]['positionY'] += float(paddles[position]['velocity'])

				rooms[self.room_id][position]['info']['positionY'] = paddles[position]['positionY']
				await self.broadcast_paddle_state(position)
				break
