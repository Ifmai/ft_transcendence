from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user.api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import  GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# from user.models import RefreshToken as RefreshTokenModel
# from django.utils import timezone
# from datetime import timedelta

# class UserLogin(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
        
#         data = response.data
#         user = request.user
        
#         # Yeni refresh token oluşturuluyor
#         refresh = RefreshToken.for_user(user)
#         refresh_token = str(refresh)
        
#         # Access token'ın ömrünü belirlemek için örnek süre
#         refresh_token_lifetime = timedelta(days=7)  # Örneğin, 5 dakika
#         access_token_lifetime = timedelta(minutes=5)

#         # Refresh token modeline kaydediliyor
#         RefreshTokenModel.objects.update_or_create(
#             auth_user=user,
#             defaults={
#                 'refresh_token': refresh_token,
#                 'expires_at': timezone.now() + refresh_token_lifetime  # Geçerlilik süresi
#             }
#         )
#         access_token = data.get('access')
#         response = Response(data)
#         response.set_cookie(
#             key='access_token',
#             value=access_token,
#             httponly=False,
#             secure=True,  # HTTPS kullanıyorsanız True yapın
#             samesite='Strict',  # 'Lax' veya 'None' da kullanabilirsiniz
#             max_age=access_token_lifetime  # Cookie'nin ömrünü belirleyin
#         )
#         return response


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
        
