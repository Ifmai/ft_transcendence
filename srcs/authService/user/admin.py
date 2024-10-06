from django.contrib import admin

from user.models import Profil, ProfileComment, UserFriendsList, PlayerMatch, PlayerTournament, Tournament, ChatMessage, ChatRooms, ChatUserList

class ChatMessages(admin.ModelAdmin):
    list_display = ("chatRoom", "sender", "message")

class ChatRoom(admin.ModelAdmin):
    list_display = ("roomName", "roomActive")
    list_editable = ("roomActive",)
    list_filter = ("roomActive",)

class ChatUserLists(admin.ModelAdmin):
    list_display = ("chatRoom", "user")

class TournamentList(admin.ModelAdmin):
    list_display = ("id" ,"name", "status")

admin.site.register(Profil)
admin.site.register(ProfileComment)
admin.site.register(UserFriendsList)
admin.site.register(PlayerMatch)
admin.site.register(PlayerTournament)
admin.site.register(Tournament, TournamentList)
admin.site.register(ChatMessage, ChatMessages)
admin.site.register(ChatRooms, ChatRoom)
admin.site.register(ChatUserList, ChatUserLists)