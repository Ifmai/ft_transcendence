from django.urls import path, include
from user.api.Loginviews import UserCreateView, UserLogoutView, CheckRefreshTokenView, UserIntraLoginView
from user.api.Friendsviews import FriendsAdd, FriendsList, FriendsRequestList, FriendsAccept
from user.api.RefreshpassViews import PasswordResetRequest, PasswordResetConfirm
from user.api.Profileviews import ProfilViewList, ProfilCommentViewList, ProfilPhotoUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user_profil', ProfilViewList, basename='profil_content')
router.register(r'user_commend', ProfilCommentViewList, basename='comment')
router.register(r'friends', FriendsList, basename='friends')
router.register(r'friends_requests', FriendsRequestList, basename='friends_requests')

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
	path('login42/<str:code>/', UserIntraLoginView.as_view(), name='login42'),
	path('logout/', UserLogoutView.as_view(), name='logout'),
	path('refreshpassword/', PasswordResetRequest.as_view(), name='check-refresh'),
	path('reset/<str:refresh>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
	path('profil_photo/', ProfilPhotoUpdateView.as_view(), name='photo-update'),
	path('whois/', CheckRefreshTokenView.as_view(), name='check-refresh'),


	path('', include(router.urls)),
	path('addfriends/', FriendsAdd.as_view(), name='add-friends'),
	path('acceptfriends/<int:id>/', FriendsAccept.as_view(), name='accept-friends'),
]