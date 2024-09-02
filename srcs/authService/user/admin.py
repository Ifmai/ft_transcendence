from django.contrib import admin

from user.models import Profil, ProfileComment, UserFriendsList


admin.site.register(Profil)
admin.site.register(ProfileComment)
admin.site.register(UserFriendsList)