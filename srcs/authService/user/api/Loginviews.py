from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user.api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework import status
from django.http import JsonResponse
from user.api.permissions import ApiRequestPermission
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from pprint import pprint

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ApiRequestPermission]


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        print("Request body: ", request.body)
        
        try:
            data = request.data
            print("Request data: ", data)
            username = data.get('username')
            password = data.get('password')
        except Exception as e:
            print(f"Error parsing request data: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    #permission_classes = [IsAuthenticated, ApiRequestPermission]

    def post(self, request, *args, **kwargs):
        print('gelen: ', request)
        logout(request)  # Django'nun built-in logout fonksiyonunu kullanarak oturumu sonlandır
        
        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('csrftoken')  # CSRF token çerezini sil
        response.delete_cookie('sessionid')
        return response
