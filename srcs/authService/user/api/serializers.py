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

    def validate_username(self, value):
        forbidden_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '.', ',', '<', '>', '-', ':', ';']  # yasaklı karakter listesi
        if any(char in value for char in forbidden_characters):
            raise serializers.ValidationError("The username contains forbidden characters!")
        return value

    # şifreyi kontrol etmek için
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("The password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("The password must contain at least one number.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("The password must contain at least one letter.")
        return value

    # tüm validate işlemlerini tek seferde yapmak için
    def validate(self, data):
        if data['first_name'] == data['last_name']:
            raise serializers.ValidationError("The first name and last name cannot be the same.")
        return data

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

class ProfileUpdateSerializer(serializers.ModelSerializer):
    user_first_name_update = serializers.CharField(source='user.first_name', write_only=True)
    user_last_name_update = serializers.CharField(source='user.last_name', write_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Profil
        exclude = ['otp_secret_key']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            instance.user.first_name = user_data.get('first_name', instance.user.first_name)
            instance.user.last_name = user_data.get('last_name', instance.user.last_name)
            instance.user.save()
        return super().update(instance, validated_data)

class ProfilSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    photo = serializers.ImageField(read_only=True)

    class Meta:
        model = Profil
        exclude = ['otp_secret_key']


class Profile2FCASerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Profil
        fields = '__all__'

class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = ['photo']

class ProfileCommentSerializer(serializers.ModelSerializer):
    user_profil = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfileComment
        fields = '__all__'

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LeaderBoardSerializer(serializers.Serializer):
    user = serializers.StringRelatedField(read_only=True)
    point = serializers.SerializerMethodField()
    class Meta:
        model = Profil
        fields = ['user', 'point']

    def get_point(self, profil):
        point = (profil.wins * 50) - (profil.losses * 22)
        return point