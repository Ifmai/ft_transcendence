# routing.py
from django.urls import path, re_path
from .consumers import PongConsumer

websocket_urlpatterns = [
	path('ws-pong/pong/<str:room_id>/', PongConsumer.as_asgi()),
	path('ws-pong/pong/<str:room_id>/<int:match_id>/', PongConsumer.as_asgi()),
]
