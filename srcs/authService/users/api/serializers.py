from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import UserProfile
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user

# class UserSerializers(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name']

#     def validate_email(self, value):
#         # E-posta adresinin benzersiz olduğunu doğrulama
#         if User.objects.filter(email=value).exists():
#             raise ValidationError("Bu e-posta adresi zaten kullanılıyor.")
#         return value

#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise ValidationError('Bu username zaten kullanılıyor.')
#         return value
    
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             first_name=validated_data['first_name', ' '],
#             last_name=validated_data['last_name', ' ']
#         )
#         return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    foto = serializers.ImageField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
