from django.urls import path, include
from django.contrib import admin
from user.api.Loginviews import UserCreateView, UserLogoutView, CheckRefreshTokenView
from user.api.RefreshpassViews import PasswordResetRequest, PasswordResetConfirm
from user.api.Profileviews import ProfilViewList, ProfilCommentViewList, ProfilPhotoUpdateView
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'user_profil', ProfilViewList, basename='profil_content')
router.register(r'user_commend', ProfilCommentViewList, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserCreateView.as_view(), name='register'),
	path('logout/', UserLogoutView.as_view(), name='logout'),
	path('profil_photo/', ProfilPhotoUpdateView.as_view(), name='photo-update'),
	path('whois/', CheckRefreshTokenView.as_view(), name='check-refresh'),
	path('refreshpassword/', PasswordResetRequest.as_view(), name='check-refresh'),
	path('reset/<str:refresh>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
	path('', include(router.urls)),
]