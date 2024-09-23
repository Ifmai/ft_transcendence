from django.urls import path
from .views import TournamentView, TournamentList

urlpatterns = [
	path('', TournamentView.as_view(), name='tournament-view'),
	path('get/', TournamentList.as_view(), name='tournament-list')
]
