import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import uuid
from .models import Match
from .enums import *
from asgiref.sync import sync_to_async

match_rooms = dict()

@sync_to_async
def match_played(match_id):
	try:
		match = Match.objects.get(id=match_id)
		return match.state == State.PLAYED.value
	except Match.DoesNotExist:
		return False

async def find_channels_room(player_id, channel_name):
	return None, None


class MatchMakerConsumer(AsyncWebsocketConsumer):
	async def receive(self, text_data):
		#print("text_data: ", text_data)
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
			await self.send(text_data=json.dumps({'message': 'User not authenticated', 'status': 403}))
			await self.close()
			return

		# print(f"Channel Name: {self.channel_name}")
		room, room_id = await find_channels_room(player_id, self.channel_name)
		if match_id is not None and await match_played(match_id):
			await self.send(text_data=json.dumps({'message': "Match's Already Been Played", 'status': 400}))
			return

		await self.send(text_data=json.dumps({'message': 'Connected', 'status': 200, 'match_id': match_id}))

	async def disconnect(self, close_code):
		pass

