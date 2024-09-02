# routing.py
from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/friend-list/$', consumer.FriendListConsumer.as_asgi()),
]
