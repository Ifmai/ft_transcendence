from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profil, ProfileComment

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

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
    user = serializers.StringRelatedField(read_only=True)
    foto = serializers.ImageField(read_only=True)

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

# class RefreshTokenSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)
#     class Meta:
#         model = RefreshToken
#         fields = '__all__'
