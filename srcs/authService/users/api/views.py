from rest_framework import generics
from django.contrib.auth.models import User
from users.api.serializers import CustomRegisterSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer