from django.urls import path
from user.api.views import UserListCreateView

urlpatterns = [
    path('register/', UserListCreateView.as_view(), name='register'),
]