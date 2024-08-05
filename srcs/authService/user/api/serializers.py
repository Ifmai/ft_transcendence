from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    def save(self, request ,**kwargs):
        user = super().save(**kwargs)
        user.first_name = self.request.get('first_name')
        user.last_name = self.request.get('last_name')
        user.save()
        return user