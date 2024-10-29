# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import Profil, UserFriendsList, ChatRooms, ChatUserList, Tournament
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
			self.additional_group_name = f'tournament_announce'

			await self.update_online_status('ON')
			await self.channel_layer.group_add(
            	self.room_group_name,
            	self.channel_name
			)
			await self.channel_layer.group_add(
            	self.additional_group_name,
            	self.channel_name
			)

			await self.accept()
			await self.notify_friends('ON')

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		m_type = text_data_json["type"]
		action_map = {
			'list_request': self.list_request,
			'friend_request': lambda: self.friend_Request(text_data_json['name']),
			'friend_request_response': lambda: self.friend_request_response(text_data_json['username'], text_data_json['response']),
			'friend_request_list': self.friend_request_list,
			'delete_friend': lambda: self.delete_friend(text_data_json['name']),
			'block_friend': lambda: self.block_friend(text_data_json['name']),
			'unblock_friend': lambda: self.unblock_friend(text_data_json['name']),
			'new_tournament': lambda: self.tournament_announce(text_data_json),
   		}
		action = action_map.get(m_type)
		if action:
			await action()


	async def disconnect(self, code):
		pass
		if self.user:
			await self.update_online_status('OF')
			await self.notify_friends('OF')
			await self.channel_layer.group_discard(
				self.room_group_name,
				self.channel_name
			)
			# await self.channel_layer.group_discard(
			# 	self.additional_group_name,
			# 	self.channel_layer
			# )

	async def error_broadcast(self, message):
		await self.send(text_data=json.dumps({
			'type': 'error',
			'message': message
		}))

	async def access_broadcast(self, m_type, message):
		await self.send(text_data=json.dumps({
			'type': m_type,
			'message': message
		}))

	async def tournament_broadcast(self, event):
		tournamnet_name = event['tournament_name']
		creator_name = event['creator_name']
		await self.send(text_data=json.dumps({
			'type' : 'new_tournament',
			'tournament_name' : tournamnet_name,
			'creator_alias': creator_name
		}))

	@database_sync_to_async
	def get_tournament_obj(self, tournament_id):
		return Tournament.objects.get(id=tournament_id)

	async def tournament_announce(self, text_data_json):
		tournament_id = text_data_json['tournament_id']
		tournament = await self.get_tournament_obj(tournament_id)
		creator_name = text_data_json['creator_name']
		await self.channel_layer.group_send(
        	self.additional_group_name,
			{
				'type': 'tournament_broadcast',
				'tournament_name': tournament.name,
				'creator_name': creator_name
			}
		)

	#Friends Request Response Block/Delete
	async def delete_friend(self, username):
		r_user = await self.get_user(username)
		if await self.delete_or_block_friend_db(self.user, r_user, 'delete'):
			await self.error_broadcast("Böyle bir kişi yok.")

	async def block_friend(self, username):
		r_user = await self.get_user(username)
		if await self.delete_or_block_friend_db(self.user, r_user, 'block'):
			await self.error_broadcast("Böyle bir kişi yok.")
		else:
			await self.access_broadcast("block", f"{username}")

	async def unblock_friend(self, username):
		r_user = await self.get_user(username)
		if await self.delete_or_block_friend_db(self.user, r_user, 'unblock_friend'):
			await self.error_broadcast("Sen bu kişinin bloğunu açamazsın.")
		else:
			await self.access_broadcast("unblock", f"{username}")


	@database_sync_to_async
	def delete_or_block_friend_db(self, sender, receiver, action):
		obj  = UserFriendsList.objects.get(
        	(Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
    	)
		if obj:
			if action == 'delete':
				room_name = sorted([receiver.username, sender.username])[0] + '.' +sorted([receiver.username, sender.username])[1]
				chat_room = ChatRooms.objects.get(roomName=room_name)
				chat_room.delete()
				obj.delete()
				return False
			elif action == 'block':
				obj.friend_block = True
				obj.blocked_user = self.user
				obj.save()
				return False
			elif action == 'unblock_friend':
				if obj.blocked_user == self.user:
					obj.friend_block = False
					obj.blocked_user = None
					obj.save()
					return False
				else:
					return True
		else:
			return True



	#Friends Request Response Accept/Reject

	@database_sync_to_async
	def friend_request_update(self, r_response, sender, receiver):
		try:
			f_request = UserFriendsList.objects.get(sender=sender, receiver=receiver, friend_request=False)

			if r_response == 'accept':
				room_name = sorted([sender.username, receiver.username])[0] + '.' +sorted([sender.username, receiver.username])[1]
				new_room = ChatRooms.objects.create(roomName=room_name)
				room_user_one = ChatUserList.objects.create(chatRoom=new_room, user=sender)
				room_user_two = ChatUserList.objects.create(chatRoom=new_room, user=receiver)
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
		return request_list

	async def friend_request_list(self):
		request_list = await self.get_request_list(self.user)
		for req in request_list:
			await self.send(
				text_data=json.dumps({
					"type": 'request_list',
					"user" : req['username'],
					"photo": req['photo'],
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
			room_name = sorted([friend['username'], self.user.username])[0] + '.' +sorted([friend['username'], self.user.username])[1]
			await self.send(
				text_data=json.dumps({
					"type": 'activity',
					"user" : friend['username'],
					"status": friend['is_online'],
					"photo": friend['photo'],
					"room_name": room_name,
					"blocked" : friend['friend_block'],
					'who_blocked': friend['who_blocked']
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


	@database_sync_to_async
	def get_friends(self):
		request_user = self.scope['user']
		friends = UserFriendsList.objects.filter(
				(Q(sender=request_user) | Q(receiver=request_user)) & Q(friend_request=True)
			)

		friends_data = []
		for friend in friends:
			f_blocked_user = None
			friend_user = (friend.sender if friend.sender != request_user else friend.receiver)
			friend_profile = Profil.objects.get(user=friend_user.id)
			if friend.blocked_user != None:
				f_blocked_user = friend.blocked_user.username
			status = friend_profile.status
			friends_data.append({
				'id': friend_user.id,
				'username': friend_user.username,
				'is_online': status,
				'photo': friend_profile.photo.url,
				'friend_block': friend.friend_block,
				'who_blocked': f_blocked_user
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
