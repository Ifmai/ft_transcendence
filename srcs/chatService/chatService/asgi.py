"""
ASGI config for chatService project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatService.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.channels.routing import websocket_urlpatterns
from .middleware import JwtAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LdChat.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JwtAuthMiddleware(URLRouter(
			websocket_urlpatterns
		)),
    }
)
