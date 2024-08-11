from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user.api.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    permission_classes = [ApiRequestPermission]


class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cookies = request.COOKIES
            access_token = cookies.get('access_token')
            refresh_token = cookies.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)
            response = Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

""" class RefreshToken(APIView):
    def post(self, request, *args, **kwargs):
 """