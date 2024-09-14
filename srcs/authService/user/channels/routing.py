# routing.py
from django.urls import re_path
from user.channels.consumer import FriendListConsumer

websocket_urlpatterns = [
    re_path(r'ws/friend-list/', FriendListConsumer.as_asgi()),
]
