# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import Profil, UserFriendsList
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

import json

class FriendListConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		if self.scope['user'].is_authenticated:
			self.user = self.scope['user']
			self.room_group_name = f"friend_list_{self.user.username}"

			await self.update_online_status('ON')
			await self.channel_layer.group_add(
            	self.room_group_name,
            	self.channel_name
			)
			await self.accept()
			await self.notify_friends('ON')

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		m_type = text_data_json["type"]
		if m_type == 'list_request':
			await self.list_request()
		elif m_type == 'friend_request':
			r_username = text_data_json['name']
			await self.friend_Request(r_username)
		elif m_type == 'friend_request_response':
			s_username = text_data_json['username']
			r_response = text_data_json['response']
			await self.friend_request_response(s_username, r_response)
		elif m_type == 'friend_request_list':
			await self.friend_request_list()

	async def disconnect(self, code):
		pass
		if self.user:
			await self.update_online_status('OF')
			await self.notify_friends('OF')
			await self.channel_layer.group_discard(
				self.room_group_name,
				self.channel_name
			)


	#Friends Request Response Accept/Reject

	@database_sync_to_async
	def friend_request_update(self, r_response, sender, receiver):
		try:
			f_request = UserFriendsList.objects.get(sender=sender, receiver=receiver, friend_request=False)

			if r_response == 'accept':
				f_request.friend_request = True
				f_request.save()
				return "accepted"
			
			elif r_response == 'reject':
				f_request.delete()
				return "rejected"

		except ObjectDoesNotExist:
			return "Friend Request Not Found"

	async def friend_request_response(self, s_username, r_response):
		s_user = await self.get_user(s_username)
		s_msg = await self.friend_request_update(r_response, s_user, self.user)
		await self.send(text_data=json.dumps({
			'type' : 'friend_request_response',
			'Response': s_msg
		}))


	#Friends Request List
	@database_sync_to_async
	def check_is_friend_request(self, sender, receiver):
		both_friends = UserFriendsList.objects.filter(
        	(Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
    	).exists()
		return both_friends

	@database_sync_to_async
	def get_request_list(self, user):
		requests = UserFriendsList.objects.filter(receiver=user , friend_request=False)
		request_list = []
		for req in requests:
			sender_user = req.sender
			sender_profil = Profil.objects.get(user=sender_user)
			request_list.append({
				'username': sender_user.username,
				'photo': sender_profil.photo.url
			})
		print("Request List : ", request_list)
		return request_list

	async def friend_request_list(self):
		request_list = await self.get_request_list(self.user)
		for req in request_list:
			await self.send(
				text_data=json.dumps({
					"type": 'request_list',
					"user" : req['username'],
					"photo": req['photo']
				})
			)
	#Friends Request List END


	#Friend Request 
	@database_sync_to_async
	def add_friends_list(self, sender, receiver):
		friend = UserFriendsList.objects.create(sender=sender, receiver=receiver)
		if friend:
			return True
		else:
			return False
	
	async def friend_Request(self, r_username):
		receiver = await self.get_user(r_username)
		if receiver:
			sender = self.user
			if receiver == sender:
				await self.send(text_data=json.dumps({'error' : 'kendine arkadaşlık isteği atamazsın.'}))
			elif await self.check_is_friend_request(sender, receiver):
				await self.send(text_data=json.dumps({'error' : 'Sen zaten istke atmışsın bro.'}))
			else:
				if await self.add_friends_list(sender, receiver):
					await self.send(text_data=json.dumps({'Succses' : 'Friend Request Send'}))
				else:
					await self.send(text_data=json.dumps({'Error' : 'Server error.'}))
	#Friend Request END


	#Friends online/ofline && Friends List Functions START

	async def list_request(self):
		friend_list = await self.get_friends()
		for friend in friend_list:
			await self.send(
				text_data=json.dumps({
					"type": 'activity',
					"user" : friend['username'],
					"status": friend['is_online'],
					"photo": friend['photo']
				})
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
				'is_online': status,
				'photo': friend_profile.photo.url
			})
		return friends_data
	#Friends online/ofline && Friends List Functions END

	@database_sync_to_async
	def get_user(self, username):
		r_user = User.objects.get(username=username)
		if r_user:
			return r_user
		else:
			return False
