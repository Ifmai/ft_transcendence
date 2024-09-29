import json
from django.http import JsonResponse
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import AcceptConnection
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from chat.models import Profil
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import ChatUserList, ChatMessage, ChatRooms, Profil

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def add_user_to_group(self, user, group_name):
        room, created = ChatRooms.objects.get_or_create(roomName=group_name)
        ChatUserList.objects.get_or_create(chatRoom=room, user=user)

    @database_sync_to_async
    def get_user_list(self, group_name):
        room_user_list = ChatUserList.objects.filter(chatRoom__roomName=group_name)
        return [{"id": chat_user.user.id, "username": chat_user.user.username} for chat_user in room_user_list]

    async def connect(self):
        if self.scope['user'].is_authenticated:
            self.user = self.scope['user']
            userid = self.user.id
            self.room_group_name = "global-chat"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.add_user_to_group(self.user, self.room_group_name)
            await self.accept()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        m_type = text_data_json['type']
        m_room = text_data_json['chat_room']
        print("type : ", m_type)
        print("room : ", m_room)
        if m_type == 'chat_message':
            message = text_data_json["message"]
            if m_room != 'global-chat':
                m_created = await self.add_db_message(m_room, message, self.user, 'chat')
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "sender": self.user.username, "message": message, 'chat_room': m_room},
            )
        elif m_type == 'new_chat':
            await self.get_history(m_room)

    @database_sync_to_async
    def get_profile_photo(self, username):
        profil = Profil.objects.get(user__username=username)
        return profil.photo.url

    @database_sync_to_async
    def add_db_message(self, m_room, message, user, m_type):
        room = ChatRooms.objects.get(roomName=m_room)
        msg = ChatMessage.objects.create(chatRoom=room, sender=user, message=message, type=m_type)
        if msg == False:
            return False
        else:
            return True

    @database_sync_to_async
    def get_history_from_db(self, m_room):
        msg_list = []
        room = ChatRooms.objects.get(roomName=m_room)
        msg_get = ChatMessage.objects.filter(chatRoom=room, type='chat').select_related('sender', 'chatRoom')
        print("msg get amcık herif : ", msg_get)
        if msg_get.exists():
            for message in msg_get:
                msg_list.append({
                    'chat_room': message.chatRoom.roomName,
                    'sender': message.sender.username,  
                    'sender_photo': message.sender.profil.photo.url,
                    'message': message.message,
                    'msg_type': message.type               
                })
            return msg_list
        else:
            return msg_list

    async def get_history(self, m_room):
        msg_history = await self.get_history_from_db(m_room)
        for message in msg_history:
            print('chat_room :', message)
            await self.send(text_data=json.dumps({
                'chat_room': message['chat_room'],
                'sender':  message['sender'],
                'sender_photo': message['sender_photo'],
                'message': message['message'],
                'msg_type': message['msg_type'],
                'type': 'history'
            }))

    @database_sync_to_async
    def get_chatRoom(self, room):
        print("Room name : ", room)
        r_room = ChatRooms.objects.get(roomName=room)
        return r_room

    @database_sync_to_async
    def check_user_in_room(self, room):
        room_list = ChatUserList.objects.filter(chatRoom=room, user=self.user).exists()
        return room_list

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        room = await self.get_chatRoom(event['chat_room'])
        profil_photo = await self.get_profile_photo(sender) 
        if await self.check_user_in_room(room):
            await self.send(
                text_data=json.dumps({"type": "chat", "sender": sender, "message": message, "photo": profil_photo, 'chat_room': room.roomName})
            )

    async def activity(self, event):
        sender = event["sender"]
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {"type": "activity", "sender": sender, "message": message}
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)