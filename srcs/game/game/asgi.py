"""
ASGI config for matchmaking project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from api.routing import websocket_urlpatterns
from game.middleware import JwtAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchmaking.settings')

application = ProtocolTypeRouter(
	{
		'http': get_asgi_application(),
		'websocket' : JwtAuthMiddleware(
			URLRouter(
				websocket_urlpatterns
			)
		),
	})
