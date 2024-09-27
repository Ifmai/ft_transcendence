from django.contrib import admin

from user.models import Profil, ProfileComment, UserFriendsList, PlayerMatch, PlayerTournament, Tournament, ChatMessage, ChatRooms, ChatUserList


admin.site.register(Profil)
admin.site.register(ProfileComment)
admin.site.register(UserFriendsList)
admin.site.register(PlayerMatch)
admin.site.register(PlayerTournament)
admin.site.register(Tournament)
admin.site.register(ChatMessage)
admin.site.register(ChatRooms)
admin.site.register(ChatUserList)