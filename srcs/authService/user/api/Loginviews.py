from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user.api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from dotenv import load_dotenv
import os
import requests
import secrets

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserIntraLoginView(APIView):
    def get(self, request, *args, **kwargs):
        load_dotenv()
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        redirect_uri = os.getenv('REDIRECT_URI')

        urlauth = 'https://api.intra.42.fr/oauth/token'
        urlinfo = 'https://api.intra.42.fr/v2/me'
        code = kwargs.get('code')
        data = {
            'client_id': client_id,
            'code': code,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
        }

        response = requests.post(urlauth, json=data)
        access_token = response.json().get('access_token')
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        infoResponse = requests.get(urlinfo, headers=headers).json()
        
        loginEmail = infoResponse.get('email')
        if not User.objects.filter(email=loginEmail).exists():
            userData = {
                'username' : infoResponse.get('login'),
                'email' : loginEmail,
                'first_name' : infoResponse.get('first_name'),
                'last_name' : infoResponse.get('last_name'),
                'password' :  secrets.token_urlsafe(8)
            }
            register_response = requests.post('http://userservice:8001/register/', json=userData)
            # #loginPhotoUrl = infoResponse["image"]["versions"]["large"] #Photoyu da profile aktarmak istiyom.
            # user = User.objects.create_user(
            #     username=loginUsername,
            #     email=loginEmail,
            #     first_name=loginFirstName,
            #     last_name=loginLastName,
            #     password=random_password
            # )

        user = User.objects.get(email=loginEmail)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful.'
            },
            status=status.HTTP_200_OK
        )

class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cookies = request.COOKIES
            refresh_token = cookies.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)
            response = Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CheckRefreshTokenView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            cookies = request.COOKIES
            refresh_token = cookies.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token required.'}, status=status.HTTP_202_ACCEPTED)
            return Response({'okaii'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)