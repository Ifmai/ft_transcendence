import json
from channels.generic.websocket import WebsocketConsumer

class MatchMakerConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()
		self.send(text_data=json.dumps({'message': 'Connected', 'status': 200}))
