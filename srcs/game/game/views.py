from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.http import JsonResponse

def get_test_token(request):
	user, created = User.objects.get_or_create(username='testuser', password='testpassword')

	refresh = RefreshToken.for_user(user)
	access_token = str(refresh.access_token)

	return JsonResponse({'access_token': access_token})
