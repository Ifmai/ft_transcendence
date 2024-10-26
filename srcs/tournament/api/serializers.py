from rest_framework import serializers
from .models import Tournament, Profil, Match, PlayerMatch, PlayerTournament
from django.db.models import Q
from .enums import *


class ProfilSerializer(serializers.ModelSerializer):
	photo = serializers.ImageField(read_only=True)
	user = serializers.StringRelatedField(read_only=True)
	class Meta:
		model = Profil
		fields = ['user', 'photo', 'alias_name']

class TournamentSerializer(serializers.ModelSerializer):
	matches = serializers.SerializerMethodField()
	creator = serializers.SerializerMethodField()
	player_count = serializers.SerializerMethodField()

	class Meta:
		model = Tournament
		fields = ('id', 'name', 'status', 'round', 'creator', 'player_count', 'matches')

	def is_player_in_tournament(self, player_id):
		tournament = Tournament.objects.filter(
			Q(playertournament__player=player_id) &
			(Q(status=StatusChoices.PENDING.value) |
			Q(status=StatusChoices.IN_PROGRESS.value))
		).first()
		return tournament

	def get_matches(self, tournament):
		matches = Match.objects.filter(tournament=tournament)
		serializer = MatchSerializer(matches, context={"player": self.context.get("player")}, many=True)
		return serializer.data

	def get_players(self, tournament):
		players_tournament = PlayerTournament.objects.filter(tournament=tournament)
		players = []
		for player_tournament in players_tournament:
			players.append(Profil.objects.get(id=player_tournament.player.id))
		player_data = ProfilSerializer(instance=players, many=True)
		return player_data.data

	def get_player_count(self, tournament):
		players = PlayerTournament.objects.filter(tournament=tournament)
		return players.count()

	def get_creator(self, tournament):
		player = self.context.get("player")
		return PlayerTournament.objects.filter(tournament_id=tournament, player_id=player, creator=True).exists()

class PlayerMatchSerializer(serializers.ModelSerializer):
	player = serializers.SerializerMethodField()

	class Meta:
		model = PlayerMatch
		fields = ('player', 'score', 'won')

	def get_player(self, player_match):
		player = Profil.objects.get(id=player_match.player.id)
		serializer = ProfilSerializer(player)
		return serializer.data

class MatchSerializer(serializers.ModelSerializer):
	players = serializers.SerializerMethodField()

	class Meta:
		model = Match
		fields = ('id', 'tournament', 'round', 'state', 'players')

	def get_players(self, match):
		player_matches = PlayerMatch.objects.filter(match_id=match.id)
		serializer = PlayerMatchSerializer(player_matches, many=True)
		return serializer.data

class TournamentListSerializer(serializers.ModelSerializer):
    player_aliases = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'player_aliases']

    def get_player_aliases(self, tournament):
        players_tournament = PlayerTournament.objects.filter(tournament=tournament, creator=True)
        return players_tournament[0].player.alias_name if players_tournament else None


class MatchHistorySerializer(serializers.ModelSerializer):
	players = serializers.SerializerMethodField()

	class Meta:
		model = Match
		fields = ('id', 'players')

	def get_players(self, match):
		player_matches = PlayerMatch.objects.filter(match_id=match.id)
		serializer = PlayerMatchSerializer(player_matches, many=True)
		return serializer.data