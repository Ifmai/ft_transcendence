from django.contrib import admin

from user.models import Profil, ProfileComment, UserFriendsList, PlayerMatch, PlayerTournament, Tournament


admin.site.register(Profil)
admin.site.register(ProfileComment)
admin.site.register(UserFriendsList)
admin.site.register(PlayerMatch)
admin.site.register(PlayerTournament)
admin.site.register(Tournament)