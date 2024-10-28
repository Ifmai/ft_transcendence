import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import uuid
from .models import Match, PlayerTournament, Tournament, Profil
from .enums import *
from asgiref.sync import sync_to_async

game_rooms = dict()

@sync_to_async
def match_played(match_id):
	try:
		match = Match.objects.get(id=match_id)
		return match.state == State.PLAYED.value
	except Match.DoesNotExist:
		return False

async def find_channels_room(player_id, channel_name):
	"""
	This function finds the room that the player is in.
	"""
	for room_id, room in game_rooms.items():
		for player in room['players']:
			if player_id in player and player[player_id] == channel_name:
				room['players'].remove(player)
				return room, room_id
	return None, None

async def create_room(player_id, channel_name, capacity, match_id):
	"""
	This function creates a game room for the player.
	"""
	room_id = str(uuid.uuid4())
	game_rooms[room_id] = {
		"players": [{player_id: channel_name}],
		"match_id": match_id,
		"capacity": capacity
	}
	return game_rooms[room_id], room_id

async def get_room(player_id, capacity, channel_name, match_id):
	"""
	This function retrieves or creates a game room for the player.
	"""
	for room_id, room in game_rooms.items():
		if any(player_id in player for player in room['players']):
			return None, None
		if len(room['players']) < capacity and room['capacity'] == capacity and room['match_id'] == match_id:
			room['players'].append({player_id: channel_name})
			await get_channel_layer().group_add(room_id, channel_name)

			if len(room['players']) == capacity:
				await get_channel_layer().group_send(room_id, {
					'type': 'game_start_message',
					'text': "The game is starting",
					'room_id': room_id,
				})
				del game_rooms[room_id]
			return room, room_id
		elif len(room['players']) == capacity and room['capacity'] == capacity and room['match_id'] == match_id:
			return None, None
	return await create_room(player_id, channel_name, capacity, match_id)

@sync_to_async
def is_tournament_creator(player_id):
	player_tournament = PlayerTournament.objects.filter(player_id=player_id, creator=True).first()
	return player_tournament is not None

@sync_to_async
def delete_tournament(player_id):
	player_tournament = PlayerTournament.objects.filter(player_id=player_id, creator=True).first()
	if player_tournament:
		Tournament.objects.filter(id=player_tournament.tournament_id).delete()

class MatchMakerConsumer(AsyncWebsocketConsumer):
	async def game_start_message(self, event):
		await self.send(text_data=json.dumps({
			'room_id': event['room_id'],
			'text' : event['text']
		}))

	async def disconnect_message_author(self, event):
		await self.send(text_data=json.dumps({
			'text' : event['text'],
			'status': event['status']
		}))

	async def receive(self, text_data):
		try:
			data = json.loads(text_data)
		except json.JSONDecodeError as e:
			print(f"JSON decode error: {e}")
			await self.send(text_data=json.dumps({'message': 'Invalid JSON', 'error': str(e)}))
			return
		await self.send(text_data=json.dumps({'message': 'Received', 'data': data}))

	async def connect(self):
		await self.accept()
		try:
			match_id = self.scope['url_route']['kwargs'].get('match_id')
			capacity =  self.scope['url_route']['kwargs'].get('capacity')
		except KeyError as e:
			print(f"Error getting scope: {e}")

		if self.scope['user']:
			player_id = self.scope['user'].id
		else:
			await self.send(text_data=json.dumps({'message': 'User not authenticated', 'status': 401}))
			await self.close()
			return

		if match_id is not None and await match_played(match_id):
			await self.send(text_data=json.dumps({'message': "Match's Already Been Played", 'status': 400}))
			return

		existing_room, existing_room_id = await find_channels_room(player_id, self.channel_name)
		if existing_room is not None:
			await self.channel_layer.group_discard(existing_room_id, self.channel_name)
			await self.send(text_data=json.dumps({'message': 'Disconnected from previous room', 'status': 200}))
			return

		room, room_id = await get_room(player_id, capacity, self.channel_name, match_id)
		if not room:
			await self.send(text_data=json.dumps({'message': 'No room found or player already in the queue', 'status': 400}))
			return

		await self.channel_layer.group_add(room_id, self.channel_name)

		player_alias_map = {}
		for player in room['players']:
			player_id_in_room = list(player.keys())[0]
			profil = await sync_to_async(Profil.objects.get)(user_id=player_id_in_room)
			player_alias_map[player_id_in_room] = profil.alias_name

		await self.send(text_data=json.dumps({
			'message': 'Connected',
			'status': 200,
			'match_id': match_id,
			'players': player_alias_map
		}))

		await self.broadcast_alias_name(room_id, player_alias_map)

	async def disconnect(self, close_code):
		if self.scope['user']:
			player_id = self.scope['user'].id
		else:
			return
		room, room_id = await find_channels_room(player_id, self.channel_name)
		if room:
			if await is_tournament_creator(player_id):
				await delete_tournament(player_id)
				await get_channel_layer().group_send(room_id, {
					'type': 'disconnect_message_author',
					'text': "Creator of the tournament left",
					'status': 200
				})
			await self.channel_layer.group_discard(room_id, self.channel_name)

	async def broadcast_alias_name(self, room_id, player_alias_map):
		await self.channel_layer.group_send(room_id, {
			'type': 'alias_names_message',
			'players': player_alias_map})

	async def alias_names_message(self, event):
		await self.send(text_data=json.dumps({
			'message': 'Updated player list',
			'players': event['players']
			}))
