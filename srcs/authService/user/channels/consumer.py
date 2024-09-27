# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import Profil, UserFriendsList
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from django.db.models import Q

import json

class FriendListConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		print("self scope : ", self.scope['user'])
		if self.scope['user'].is_authenticated:
			self.user = self.scope['user']
			self.room_group_name = f"friend_list_{self.user.username}"

			await self.update_online_status('ON')
			await self.channel_layer.group_add(
            	self.room_group_name,
            	self.channel_name
			)
			await self.accept()
			await self.notify_friends('online')
	
	async def disconnect(self, code):
		pass
		if self.user:
			await self.update_online_status('OF')
			await self.notify_friends('offline')
			await self.channel_layer.group_discard(
				self.room_group_name,
				self.channel_name
			)

	async def notify_friends(self, status):
		friends = await self.get_friends()
		for friend in friends:
			room_group_name = f"friend_list_{friend['username']}"  # friend['username'] olarak güncellendi
			await self.channel_layer.group_send(
				room_group_name,
				{
					'type': 'friend_status',
					'status': status,
					'username': self.scope['user'].username
				}
			)

	async def friend_status(self, event):
		await self.send(text_data=json.dumps({
            'type': 'friend_status',
            'username': event['username'],
            'status': event['status'],
        }))

	async def update_online_status(self, change_status):
		user = self.scope['user']
		
		if user.is_authenticated:
			await sync_to_async(Profil.objects.filter(user=user).update)(status=change_status)

	async def get_friends(self):
		request_user = self.scope['user']
		friends = await sync_to_async(lambda: list(
			UserFriendsList.objects.filter(
				(Q(sender=request_user) | Q(receiver=request_user)) & Q(friend_request=True)
			)
		))()

		friends_data = []
		for friend in friends:
			friend_user = await sync_to_async(lambda: friend.sender if friend.sender != request_user else friend.receiver)()
			friend_profile = await sync_to_async(lambda: Profil.objects.get(user=friend_user.id))()
			status = friend_profile.status
			friends_data.append({
				'id': friend_user.id,
				'username': friend_user.username,
				'is_online': status
			})
		return friends_data