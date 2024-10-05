from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from api.models import Profil
import random

User = get_user_model()

def get_test_token(request):
    random_username = f'testuser_{random.randint(1000, 9999)}'
    user, created = User.objects.get_or_create(username=random_username, defaults={'password': 'testpassword'})

    if created or not hasattr(user, 'profil'):
        Profil.objects.create(user=user)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return JsonResponse({'access_token': access_token})
