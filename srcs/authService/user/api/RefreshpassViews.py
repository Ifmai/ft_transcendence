from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from cryptography.fernet import Fernet
import os

KEY = os.getenv('FERNET_KEY').encode()

def encrypt_data(data):
    fernet = Fernet(KEY)
    encrypted = fernet.encrypt(data.encode())
    return encrypted.decode()

def decrypt_data(encrypted_data):
    fernet = Fernet(KEY)
    decrypted = fernet.decrypt(encrypted_data.encode())
    return decrypted.decode()

class PasswordResetRequest(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email field is required."}, status=status.HTTP_400_BAD_REQUEST)
        userobj = User.objects.filter(email=email).first()
        if not userobj:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        token = default_token_generator.make_token(userobj)
        encrypted_pk = encrypt_data(str(userobj.pk))
        combined_token = f"{encrypted_pk}.{token}"
        reset_url = f"https://10.11.22.5/new-password?refresh={combined_token}"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_url}",
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirm(APIView):
    def post(self, request, *args, **kwargs):
        new_password = request.data['new_password']
        token = kwargs.get('refresh')
        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            encrypted_pk, token_part = token.split('.')
        except ValueError:
            return Response({"error": "Invalid token format."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decrypted_pk = decrypt_data(encrypted_pk)
        except Exception as e:
            print("Decryption error:", e)
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(pk=decrypted_pk)
        if not default_token_generator.check_token(user, token_part):
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
