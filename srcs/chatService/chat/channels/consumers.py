import json
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import AcceptConnection
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("anneni yicem birazdan.")
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print("message:", message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "sender": self.user, "message": message},
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        await self.send(
            text_data=json.dumps({"type": "chat", "sender": sender, "message": message})
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
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "activity", "sender": self.user, "message": "left"},
        )


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         # get the session daha from the scope
#         self.user = self.scope["session"]["username"]
#         userid = 0
#         for u in UsersList:
#             if u.username == self.user:
#                 userid = u.id
#                 break
#         print(f"User {self.user} connected with id {userid}")
#
#         self.room_group_name = "GlobalChat"
#         self.channel_layer.group_add(self.room_group_name, self.channel_name)
#
#         self.accept()
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         print("message:", message)
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )
#
#     def chat_message(self, event):
#         message = event["message"]
#         self.send(text_data=json.dumps({"type": "chat", "message": message}))
