from django.urls import path
from .consumers import TournamentConsumer

websocket_urlpatterns = [
    path('ws-tournament/<int:tournament_id>/', TournamentConsumer.as_asgi()),
]