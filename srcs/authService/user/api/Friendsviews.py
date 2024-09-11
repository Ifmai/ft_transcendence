from rest_framework import generics, mixins
from django.contrib.auth.models import User
from user.models import UserFriendsList
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import  GenericViewSet
from user.api.serializers import UserFriendsListIdSerializer, UserRequestListSerializer, UserFriendListSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import json

class FriendsAccept(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = UserFriendsListIdSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserFriendsList.objects.get(id=self.kwargs['id'])

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.friend_request = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class FriendsAdd(generics.CreateAPIView):
    serializer_class = UserFriendsListIdSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        add_username = request.data.get('username')

        if not add_username:
            Response({'Error': 'Pls input username.'}, status=status.HTTP_400_BAD_REQUEST)
        receiver = User.objects.get(username=add_username)
        if not receiver:
            Response({'Error': f'No user with this name {add_username} was found.'}, status=status.HTTP_400_BAD_REQUEST)
        sender = request.user
        data = {
            'sender': sender.id,
            'receiver': receiver.id
        }
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer=serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FriendsList(mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserFriendListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserFriendsList.objects.filter(
        Q(sender=self.request.user) | Q(receiver=self.request.user),
        friend_request=True
    )
    
class FriendsRequestList(mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserRequestListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserFriendsList.objects.filter(receiver=self.request.user , friend_request=False)