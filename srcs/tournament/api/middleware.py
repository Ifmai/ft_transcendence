import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from api.models import Profil

User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload['user_id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return None

@database_sync_to_async
def get_profile(user):
    try:
        profile = Profil.objects.get(user=user)
        return profile
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return None

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        
        if token:
            user = await get_user(token[0])
            profile = await get_profile(user)
            scope["user"] = user
            scope["profile"] = profile
        else:
            scope["user"] = None

        return await super().__call__(scope, receive, send)
