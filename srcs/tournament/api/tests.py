from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from .models import Tournament, Profil, PlayerTournament, Match, PlayerMatch, User
from .enums import StatusChoices, TOURNAMENT_SIZE, State
from .views import create_match, update_tournament
from .serializers import TournamentSerializer, MatchSerializer

class TournamentViewTestCase(TestCase):
    def setUp(self):
        # Create a user and generate a token for authentication
        self.user = User.objects.create_user(email='testuser@example.com', password='password', username='testuser')
        self.profil = Profil.objects.create(user=self.user, alias_name='zort')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.tournament = Tournament.objects.create(name="Tournament", status=StatusChoices.IN_PROGRESS.value)

        # Sample tournaments
        self.pending_tournament = Tournament.objects.create(name="Pending Tournament", status=StatusChoices.PENDING.value)
        self.finished_tournament = Tournament.objects.create(name="Finished Tournament", status=StatusChoices.FINISHED.value)
        self.progressing_tournament = Tournament.objects.create(name="Progressing Tournament", status=StatusChoices.IN_PROGRESS.value)


        self.players = []
        for i in range(TOURNAMENT_SIZE):
            user = User.objects.create_user(username=f'player{i}', password='testpass', email=f'player{i}@gmail.com')
            player = Profil.objects.create(user=user, alias_name=f'player{i}zort')
            PlayerTournament.objects.create(player=player, tournament=self.tournament, creator=False)
            self.players.append(player)

        self.context = {"player": self.players[0]}

    def test_get_pending_tournaments(self):
        response = self.client.get(reverse('tournament-view'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('tournaments', response.data)
        self.assertEqual(len(response.data['tournaments']), 1)
        self.assertEqual(response.data['tournaments'][0]['name'], "Pending Tournament")

    def test_no_pending_tournaments(self):
        Tournament.objects.all().delete()
        response = self.client.get(reverse('tournament-view'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], "No Tournaments available")

    def test_create_tournament(self):
        response = self.client.post(reverse('tournament-view'),
                                     data={'action': 'create',
                                        'alias_name': self.profil.alias_name,
                                        'tournament_name': 'Test Tournament'})
        self.assertEqual(response.status_code, 201)

    def test_join_tournament(self):
        response = self.client.post(reverse('tournament-view'),
                                    data={
                                        'action': 'join',
                                        'tournament_id': self.pending_tournament.id,
                                        'alias_name': self.profil.alias_name
                                    },
                                    format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Player joined tournament")

    def test_join_tournament_without_alias(self):
        response = self.client.post(reverse('tournament-view'),
                                    data={
                                        'action': 'join',
                                        'tournament_id': self.pending_tournament.id
                                    },
                                    format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Tournament is full or alias missing")

    def test_join_progressing_tournament(self):
        response = self.client.post(reverse('tournament-view'),
                                    data={
                                        'action': 'join',
                                        'tournament_id': self.progressing_tournament.id,
                                        'alias_name': self.profil.alias_name
                                    },
                                    format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Tournament is full or alias missing")

    def test_leave_tournament(self):
          PlayerTournament.objects.create(player=self.profil, tournament=self.pending_tournament, creator=False)
          response = self.client.post(reverse('tournament-view'),
                                      data={
                                          'action': 'leave',
                                          'tournament_id': self.pending_tournament.id
                                          },
                                          format='json')
          self.assertEqual(response.status_code, 200)
          self.assertEqual(response.data['message'], f"{self.profil.alias_name} left tournament")

    def test_leave_tournament_in_progress(self):
        PlayerTournament.objects.create(player=self.profil, tournament=self.progressing_tournament, creator=False)
        response = self.client.post(reverse('tournament-view'), data={
            'action': 'leave',
            'tournament_id': self.progressing_tournament.id
        },
        format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Cannot leave a tournament in progress')

    def test_leave_tournament_as_creator(self):
        PlayerTournament.objects.create(player=self.profil, tournament=self.pending_tournament, creator=True)
        response = self.client.post(reverse('tournament-view'), data={
            'action': 'leave',
            'tournament_id': self.pending_tournament.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], f'{self.profil.alias_name} left tournament')
        self.assertFalse(Tournament.objects.filter(id=self.pending_tournament.id).exists())

    def test_start_tournament(self):
        self.tournament.status = StatusChoices.PENDING.value
        self.tournament.save()
        response = self.client.post(reverse('tournament-view'), data={
            'action': 'start',
            'tournament_id': self.tournament.id
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Tournament started successfully')
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.status, StatusChoices.IN_PROGRESS.value)

    def test_update_tournament_advances_round(self):
        match1 = create_match(self.tournament, self.players[0], self.players[1])
        match2 = create_match(self.tournament, self.players[2], self.players[3])

        # Mark players 0 and 2 as winners
        PlayerMatch.objects.filter(match=match1, player=self.players[0]).update(won=True)
        PlayerMatch.objects.filter(match=match2, player=self.players[2]).update(won=True)
        Match.objects.filter(id__in=[match1.id, match2.id]).update(state=State.PLAYED.value)

        match1.refresh_from_db()
        match2.refresh_from_db()

        update_tournament(self.tournament.id)

        # Check that the tournament round has progressed
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.round, 2)

        # Check that a match has been created between the winners of round 1
        final_match = Match.objects.filter(tournament=self.tournament, round=2).first()
        self.assertIsNotNone(final_match)
        self.assertIn(self.players[0], [pm.player for pm in PlayerMatch.objects.filter(match=final_match)])
        self.assertIn(self.players[2], [pm.player for pm in PlayerMatch.objects.filter(match=final_match)])


    def test_tournament_finishes(self):
        match1 = create_match(self.tournament, self.players[0], self.players[1])
        match2 = create_match(self.tournament, self.players[2], self.players[3])

        # Mark players 0 and 2 as winners
        PlayerMatch.objects.filter(match=match1, player=self.players[0]).update(won=True)
        PlayerMatch.objects.filter(match=match2, player=self.players[2]).update(won=True)
        Match.objects.filter(id__in=[match1.id, match2.id]).update(state=State.PLAYED.value)

        match1.refresh_from_db()
        match2.refresh_from_db()

        update_tournament(self.tournament.id)

        # Create final match for the second round
        final_match = Match.objects.filter(tournament=self.tournament, round=2).first()
        Match.objects.filter(id=final_match.id).update(state=State.PLAYED.value)
        PlayerMatch.objects.filter(match=final_match, player=self.players[0]).update(won=True)

        # Call update_tournament again to finish the tournament
        update_tournament(self.tournament.id)

        # Check that the tournament is finished
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.status, StatusChoices.FINISHED.value)

    def test_get_matches(self):
        # Create matches before fetching
        self.match1 = create_match(self.tournament, self.players[0], self.players[1])
        self.match2 = create_match(self.tournament, self.players[2], self.players[3])

        self.assertEqual(Match.objects.filter(tournament=self.tournament).count(), 2)
        serializer = TournamentSerializer(context=self.context)
        matches_data = serializer.get_matches(self.tournament)

        expected_data = MatchSerializer([self.match1, self.match2], context=self.context, many=True).data
        self.assertEqual(matches_data, expected_data)
