from django.urls import path
from user.api.views import UserCreateView, UserLogoutView, custom_logout

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
]