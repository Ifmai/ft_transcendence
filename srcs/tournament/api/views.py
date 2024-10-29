from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .enums import *
from .models import Tournament, Profil, PlayerTournament, Match, PlayerMatch
from .serializers import TournamentSerializer, TournamentListSerializer, MatchHistorySerializer
from itertools import cycle
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

class TournamentList(ListAPIView):
	serializer_class = TournamentListSerializer
	queryset = Tournament.objects.filter(status=StatusChoices.PENDING.value)
	permission_classes = [IsAuthenticated]


class MatchHistoryView(ListAPIView):
	serializer_class = MatchHistorySerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		username = self.kwargs.get('username', None)
		profile = None
		if username:
			profile = Profil.objects.get(user__username=username)
		else:
			profile = Profil.objects.get(user=self.request.user)
		return Match.objects.filter(playermatch__player=profile).distinct().order_by('-id')[:8]


def create_match(tournament, player1, player2):
	new_match = Match.objects.create(tournament= tournament,
								round = tournament.round)

	PlayerMatch.objects.bulk_create([
		PlayerMatch(match=new_match, player=player1),
		PlayerMatch(match=new_match, player=player2)
	])
	return new_match

def finish_tournament(tournament, current_round_matches):
	winner_data = PlayerMatch.objects.filter(match__in=current_round_matches, won=True).first()
	winner = winner_data.player
	winner.championships += 1
	winner.save()

	tournament.status = StatusChoices.FINISHED.value
	tournament.save()

def prepare_next_round(tournament, matches):
	winners = [pm.player for pm in PlayerMatch.objects.filter(match__in=matches, won=True)]

	if len(winners) < 2:
		return

	tournament.round += 1
	tournament.save()

	while len(winners) >= 2:
		player1 = winners.pop(0)
		player2 = winners.pop(0)
		create_match(tournament, player1, player2)

def update_tournament(tournament_id):
	tournament = Tournament.objects.select_related().get(id=tournament_id)

	if tournament.status == StatusChoices.FINISHED.value:
		return

	current_round_matches = Match.objects.filter(tournament=tournament, round=tournament.round)

	if all(match.state == State.PLAYED.value for match in current_round_matches):
		winning_players = PlayerMatch.objects.filter(match__in=current_round_matches, won=True)
		if len(winning_players) == 1:
			finish_tournament(tournament, current_round_matches)
		else:
			prepare_next_round(tournament, current_round_matches)

class TournamentView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		# Get Player Data
		user_id = request.user.id
		player = Profil.objects.get(user_id=user_id)
		serializer = TournamentSerializer()
		current_tournament = serializer.is_player_in_tournament(player.id)

		if current_tournament:
			serializer = TournamentSerializer(current_tournament, context={"player": player})
			if current_tournament.status == StatusChoices.PENDING.value:
				return Response({"statusCode": 200,
					"current_tournament": serializer.data,
					"players": serializer.get_players(current_tournament)},
					status=status.HTTP_200_OK)
			update_tournament(current_tournament.id)
			return Response({"statusCode": 200,
					"current_tournament": serializer.data})


		# Handle case where no tournament is available
		tournaments = Tournament.objects.filter(status=StatusChoices.PENDING.value)
		if not tournaments.exists():
			return Response({"statusCode": 404, "message": "No Tournaments available"}, status=status.HTTP_404_NOT_FOUND)

		serializer = TournamentSerializer(tournaments, many=True)
		return Response({"statusCode": 200, "tournaments": serializer.data}, status=status.HTTP_200_OK)

	def post(self, request):
		action = request.data.get('action')
		user_id = request.user.id

		try:
			player = Profil.objects.get(user_id=user_id)
		except Profil.DoesNotExist:
			return Response({"statusCode": 400, "message": "Player does not exist"})

		if action == 'create':
			return self.create_tournament(request, player)

		tournament_id = request.data.get('tournament_id')
		alias = request.data.get('alias_name')

		try:
			tournament = Tournament.objects.get(id=tournament_id)
		except Tournament.DoesNotExist:
			return Response({"statusCode": 400, "message": "Tournament does not exist"})

		if action == 'join':
			return self.join_tournament(tournament, player, alias)

		if (action == 'leave'):
			return self.leave_tournament(tournament, player)

		if (action == 'start'):
			return self.start_tournament(tournament, player)

	def create_tournament(self, request, player):
		name = request.data.get('tournament_name')
		alias = request.data.get('alias_name')

		if not name or not alias:
			return Response({"statusCode": 400, "message": "Invalid Tournament name or alias"}, status=status.HTTP_400_BAD_REQUEST)

		serializer = TournamentSerializer()
		if serializer.is_player_in_tournament(player.id):
			return Response({"statusCode": 400, "message": "Player already in a tournament"}, status=status.HTTP_400_BAD_REQUEST)

		if Profil.objects.filter(alias_name=alias).exists():
			return Response({"statusCode": 400, "message": "Alias name is already taken"}, status=status.HTTP_400_BAD_REQUEST)

		tournament = Tournament.objects.create(name=name)
		PlayerTournament.objects.create(player=player, tournament=tournament, creator=True)

		player.alias_name = alias
		player.save()

		serializer = TournamentSerializer(tournament)
		return Response({
			"statusCode": 201,
			"message": "Tournament created successfully",
			"current_tournament": serializer.get_players(tournament),
			"tournament_id": tournament.id
			}, status=201)

	def join_tournament(self, tournament, player, alias):
		if alias is None or tournament.status != StatusChoices.PENDING.value:
			return Response({"statusCode": 400, "message": "Tournament is full or alias missing"}, status=status.HTTP_400_BAD_REQUEST)

		if Profil.objects.filter(alias_name=alias).exists():
			return Response({"statusCode": 400, "message": "Alias name is already taken"}, status=status.HTTP_400_BAD_REQUEST)

		serializer = TournamentSerializer()
		if (serializer.is_player_in_tournament(player.id)):
			return Response({"statusCode": 400, "message": "Player already in a tournament"}, status=status.HTTP_400_BAD_REQUEST)

		player.alias_name = alias
		player.save()

		PlayerTournament.objects.create(player=player, tournament=tournament, creator=False)
		return Response({"statusCode": 200, "message": "Player joined tournament", "tournament_id" : tournament.id}, status=status.HTTP_200_OK)
