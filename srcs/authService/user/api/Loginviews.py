from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user.models import Profil
from django.contrib.auth import authenticate
from user.api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.files.base import ContentFile
from dotenv import load_dotenv
import pyotp
import os
import requests
import secrets

class UserLoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def check_2fa_code(self, userSecretKey, code):
        totp = pyotp.TOTP(userSecretKey)
        totp.now()

        if totp.verify(code) == True:
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        code_2fa = request.data.get("code_2fa")
        user_check = authenticate(username=username, password=password)
        if user_check is not None:
            user = User.objects.get(username=username)
            userProfil = Profil.objects.get(user=user)
            if userProfil.two_factory == True and code_2fa == "":
                return Response({"2fa gereklidir"}, status=status.HTTP_202_ACCEPTED)
            elif userProfil.two_factory == True and code_2fa is not None:
                check_code = self.check_2fa_code(userProfil.otp_secret_key, code_2fa)
                if  check_code == True:
                    return super().post(request, *args, **kwargs)
                else:
                    return Response({"2fa kodu yanlış"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return super().post(request, *args, **kwargs)
        else:
            return Response({"Hatalı giriş. Şifrenizi kontrol ediniz."}, status=status.HTTP_401_UNAUTHORIZED)


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
            random_password = secrets.token_urlsafe(8)
            loginUsername = infoResponse.get('login')
            loginFirstName = infoResponse.get('first_name')
            loginLastName = infoResponse.get('last_name')
            user = User.objects.create_user(
                username=loginUsername,
                email=loginEmail,
                first_name=loginFirstName,
                last_name=loginLastName,
                password=random_password
            )
            profil = Profil.objects.get(user=user)
            url = infoResponse["image"]["versions"]["large"]
            response = requests.get(url)
            if response.status_code == 200:
                if profil:
                    photoname = infoResponse.get('login') + '.jpg'
                    profil.photo.save(photoname, ContentFile(response.content))
                    profil.save()
                else:
                    print("Profile instance not found.")
            else:
                print("Photo download failed.")
        else:
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
            headers = dict(request.headers)
            refresh_token = cookies.get('refresh_token')
            access_token = headers.get('Authorization')
            if not refresh_token:
                return Response({'error': 'Refresh token required.'}, status=status.HTTP_202_ACCEPTED)
            elif not access_token and refresh_token:
                return Response({"okaii"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'okaii'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
