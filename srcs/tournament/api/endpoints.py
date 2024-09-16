from django.urls import path
from .views import TournamentView

urlpatterns = [
	path('', TournamentView.as_view(), name='tournament-view'),
]
