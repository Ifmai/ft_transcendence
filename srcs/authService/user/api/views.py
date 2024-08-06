from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from user.api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework import status
from django.http import JsonResponse


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        logout(request)  # Django'nun built-in logout fonksiyonunu kullanarak oturumu sonlandır
        
        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('csrftoken')  # CSRF token çerezini sil
        response.delete_cookie('sessionid')
        return response


def get_request_info(request):
    origin = request.META.get('HTTP_ORIGIN', 'Unknown origin')
    referer = request.META.get('HTTP_REFERER', 'Unknown referer')
    
    data = {
        'origin': origin,
        'referer': referer
    }
    
    return JsonResponse(data)