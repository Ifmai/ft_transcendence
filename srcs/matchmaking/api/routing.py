# routing.py
from django.urls import path, re_path
from .consumers import MatchMakerConsumer

websocket_urlpatterns = [
	re_path(r'ws/matchmaking/$', MatchMakerConsumer.as_asgi()),
	path('ws/matchmaking/<int:capacity>/<int:match_id>/', MatchMakerConsumer.as_asgi()),
	path('ws/matchmaking/<int:capacity>/', MatchMakerConsumer.as_asgi()),
]
