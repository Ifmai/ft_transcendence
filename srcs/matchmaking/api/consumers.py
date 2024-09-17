import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import uuid
#from .models import Match

class MatchMakerConsumer(AsyncWebsocketConsumer):
	async def receive(self, text_data):
		print("text_data: ", text_data)
		await self.send(text_data=json.dumps({'message': 'Received', 'data': text_data}))

	async def connect(self):
		try:
			match_id = self.scope['url_route']['kwargs'].get('match_id')
			capacity =  self.scope['url_route']['kwargs'].get('capacity')
		except KeyError as e:
			print(f"Error getting scope: {e}")

		await self.accept()
		await self.send(text_data=json.dumps({'message': 'Connected', 'status': 200, 'match_id': match_id}))

	async def disconnect(self, close_code):
		pass

