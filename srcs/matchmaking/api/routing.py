# routing.py
from django.urls import path, re_path
from .consumers import MatchMakerConsumer

websocket_urlpatterns = [
	path('ws/matchmaking/<int:capacity>/<int:match_id>/', MatchMakerConsumer.as_asgi()),
	path('ws/matchmaking/<int:capacity>/', MatchMakerConsumer.as_asgi()),
]
