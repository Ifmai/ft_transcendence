from django.urls import path, include
from django.contrib import admin
from user.api.Loginviews import UserCreateView, UserLogoutView, LoginView
from user.api.Profileviews import ProfilViewList, ProfilCommentViewList, ProfilPhotoUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user-profil', ProfilViewList)
router.register(r'user-commend', ProfilCommentViewList, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserCreateView.as_view(), name='register'),
	path('logout/', UserLogoutView.as_view(), name='logout'),
	path('login/', LoginView.as_view(), name='login'),
	path('profil_photo/', ProfilPhotoUpdateView.as_view(), name='photo-update'),
	path('', include(router.urls)),
]