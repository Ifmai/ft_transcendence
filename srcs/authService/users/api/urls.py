# users/api/urls.py
from django.urls import path
from .views import UserListCreateView

urlpatterns = [
    path('register/', UserListCreateView.as_view(), name='register'),
]