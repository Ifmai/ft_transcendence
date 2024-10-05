from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from api.models import Profil

User = get_user_model()

def get_test_token(request):
    # Get or create a test user
    user, created = User.objects.get_or_create(username='testuser', defaults={'password': 'testpassword'})

    # Ensure the Profil exists for this user
    if created or not hasattr(user, 'profil'):
        Profil.objects.create(user=user)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return JsonResponse({'access_token': access_token})
