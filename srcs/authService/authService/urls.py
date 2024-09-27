"""
URL configuration for authService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib import admin
from user.api.Loginviews import UserLoginView
from user.api.Profileviews import serve_dynamic_image, serve_dynamic_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('user.api.urls')),
	path('api/users/jwtlogin/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/static/<str:filename>/', serve_dynamic_image, name='serve_dynamic_image'),
    path('api/users/media/profil_photo/<str:filename>/', serve_dynamic_media, name='serve_dynamic_media'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG == True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)