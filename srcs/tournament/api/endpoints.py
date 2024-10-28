from django.urls import path
from .views import TournamentView, TournamentList, MatchHistoryView

urlpatterns = [
	path('', TournamentView.as_view(), name='tournament-view'),
	path('get/', TournamentList.as_view(), name='tournament-list'),
    path('match-history/', MatchHistoryView.as_view(), name='match-history'),
	path('match-history/<str:username>/', MatchHistoryView.as_view(), name='match-history-user'),
]
