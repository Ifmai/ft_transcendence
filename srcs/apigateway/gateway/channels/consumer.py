# consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

class FriendListConsumer(WebsocketConsumer):
	def connect(self):
		print('connect : ', self)