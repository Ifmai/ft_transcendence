from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user.api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework import status

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)  # Django'nun built-in logout fonksiyonunu kullanarak oturumu sonlandır
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logged out successfully'})
    return Response({'error': 'Invalid method'}, status=405)