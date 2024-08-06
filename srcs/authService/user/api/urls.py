from django.urls import path
from user.api.views import UserCreateView, UserLogoutView, get_request_info

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
	path('logout/', UserLogoutView.as_view(), name='logout'),
    path('request-info/', get_request_info, name='get_request_info'),
]