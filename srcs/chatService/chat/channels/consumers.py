import json
from django.http import JsonResponse
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import AcceptConnection
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from chat.models import Profil
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import ChatUserList, ChatMessage, ChatRooms

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
        print("self scope : ", self.scope['user'])
        if self.scope['user'].is_authenticated:
            self.user = self.scope['user']
            userid = self.user.id
            print(f"User {self.user} connected with id {userid}")

            self.room_group_name = "GlobalChat"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.add_user_to_group(self.user, self.room_group_name)
            await self.accept()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("gelen data : ", text_data_json)
        message = text_data_json["message"]
        print("message:", message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "sender": self.user.username, "message": message},
        )

    @database_sync_to_async
    def get_profile_photo(self, username):
        profil = Profil.objects.get(user__username=username)
        return profil.photo.url

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        profil_photo = await self.get_profile_photo(sender)
        await self.send(
            text_data=json.dumps({"type": "chat", "sender": sender, "message": message, "photo": profil_photo})
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