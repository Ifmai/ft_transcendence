from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profil, ProfileComment, UserFriendsList
from rest_framework.response import Response
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        return user

class ProfilSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    photo = serializers.ImageField(read_only=True)

    class Meta:
        model = Profil
        exclude = ['otp_secret_key']
        #fields = ['id', 'user_name', 'user_email', 'bio', 'city', 'photo', 'two_factory','user_first_name', 'user_last_name']
        #fields = '__all__'

class Profile2FCASerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Profil
        fields = '__all__'

class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = ('photo')

class ProfileCommentSerializer(serializers.ModelSerializer):
    user_profil = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfileComment
        fields = '__all__'

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserFriendsListIdSerializer(serializers.ModelSerializer):
    sender_id = serializers.PrimaryKeyRelatedField(source='sender', read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(source='receiver', read_only=True)

    class Meta:
        model = UserFriendsList
        fields = ['id', 'sender', 'receiver', 'sender_id', 'receiver_id', 'friend_request', 'create_time', 'update_time']
        read_only_fields = ['create_time', 'update_time']

class UserRequestListSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = UserFriendsList
        fields = ['id', 'sender_username']

class UserFriendListSerializer(serializers.ModelSerializer):
    friend_username = serializers.SerializerMethodField()

    class Meta:
        model = UserFriendsList
        fields = ['id', 'friend_username']

    def get_friend_username(self, obj):
        if obj.sender == self.context['request'].user:
            return obj.receiver.username
        return obj.sender.username

