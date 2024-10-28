from django.urls import path, include
from user.api.Loginviews import UserCreateView, UserLogoutView, CheckRefreshTokenView, UserIntraLoginView
from user.api.RefreshpassViews import PasswordResetRequest, PasswordResetConfirm
from user.api.Profileviews import ProfilViewList, ProfilCommentViewList, ProfilPhotoUpdateView
from user.api.User2FCA import Enabled2FCA
from user.api.LeaderBoardviews import LeaderBoardView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user_profil', ProfilViewList, basename='profil_content')
router.register(r'user_commend', ProfilCommentViewList, basename='comment')

urlpatterns = [
	path('user_profil/other/<str:username>/', ProfilViewList.as_view({'get': 'list'}), name='profil_content'),
    path('register/', UserCreateView.as_view(), name='register'),
	path('login42/<str:code>/', UserIntraLoginView.as_view(), name='login42'),
	path('logout/', UserLogoutView.as_view(), name='logout'),
	path('refreshpassword/', PasswordResetRequest.as_view(), name='check-refresh'),
	path('reset/<str:refresh>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
	path('profil_photo/', ProfilPhotoUpdateView.as_view(), name='photo-update'),
	path('whois/', CheckRefreshTokenView.as_view(), name='check-refresh'),
	path('2fcaenable/', Enabled2FCA.as_view(), name='user2fca'),
	path('leaderboard/', LeaderBoardView.as_view(), name='leaderboard'),
	path('', include(router.urls)),
]