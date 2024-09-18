import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import uuid
from .models import Match
from .enums import *
from asgiref.sync import sync_to_async


@sync_to_async
def match_played(match_id):
	try:
		match = Match.objects.get(id=match_id)
		return match.state == State.PLAYED.value
	except Match.DoesNotExist:
		return False

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
		try:
			match_id = self.scope['url_route']['kwargs'].get('match_id')
			capacity =  self.scope['url_route']['kwargs'].get('capacity')
		except KeyError as e:
			print(f"Error getting scope: {e}")

		await self.accept()
		if match_id is not None and await match_played(match_id):
			await self.send(text_data=json.dumps({'message': "Match's Already Been Played", 'status': 400}))
			return

		await self.send(text_data=json.dumps({'message': 'Connected', 'status': 200, 'match_id': match_id}))

	async def disconnect(self, close_code):
		pass

