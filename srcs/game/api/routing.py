# routing.py
from django.urls import path, re_path
from .consumers import PongConsumer

websocket_urlpatterns = [
	path('ws/pong/<str:room_id>/<int:capacity>/', PongConsumer.as_asgi()),
	path('ws/pong/<str:room_id>/<int:capacity>/<int:match_id>/', PongConsumer.as_asgi()),
]