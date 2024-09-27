from django.urls import path
from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # write a path to get the chat consumer with username as a parameter
    # e.g. ws/socket-server/username/
    path(r'ws-chat/global-chat/', ChatConsumer.as_asgi()),
]