import json
from django.http import JsonResponse
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from channels.exceptions import AcceptConnection
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from itertools import cycle
from rest_framework import status
from api.enums import StatusChoices, TOURNAMENT_SIZE
from channels.generic.websocket import AsyncWebsocketConsumer
from api.models import Tournament, PlayerTournament, Match, PlayerMatch
import asyncio

tournament_dict = dict()

class TournamentConsumer(AsyncWebsocketConsumer):

	@database_sync_to_async
	def create_match(self, tournament, player1, player2):
		new_match = Match.objects.create(tournament= tournament,
									round = tournament.round)

		PlayerMatch.objects.bulk_create([
			PlayerMatch(match=new_match, player=player1),
			PlayerMatch(match=new_match, player=player2)
		])
		return {
			'match_id': new_match.id,
			'player1': player1,
			'player2': player2
		}

	async def send_private_match_id(self, match_id, player1, player2):
		if self.profile in [player1, player2]:
			await self.send(text_data=json.dumps({
				'type': 'match',
				'match_id': match_id,
				'room_name': self.room_group_name
			}))

	async def check_tournament_state(self):
		if self.tournament.status == StatusChoices.PENDING.value:
			if len(tournament_dict[self.room_group_name]['profiles']) == 4:
				player1 = tournament_dict[self.room_group_name]['profiles'][0]['profile']
				player2 = tournament_dict[self.room_group_name]['profiles'][3]['profile']
				player3 = tournament_dict[self.room_group_name]['profiles'][1]['profile']
				player4 = tournament_dict[self.room_group_name]['profiles'][2]['profile']

				match_info1 = await self.create_match(self.tournament, player1, player2)
				tournament_dict[self.room_group_name]['matches'].append(match_info1)
				match_info2 = await self.create_match(self.tournament, player3, player4)
				tournament_dict[self.room_group_name]['matches'].append(match_info2)
				self.change_tournament_state(StatusChoices.IN_PROGRESS.value)
				await get_channel_layer().group_send(
					self.room_group_name,
					{
						'type': 'broadcast_message',
						'message': 'start_match',
						'm_type': 'start'
					}
				)

	async def start_point(self):
		if len(tournament_dict[self.room_group_name]['matches']) == 2:
			for match in tournament_dict[self.room_group_name]['matches']:
				await self.send_private_match_id(match['match_id'], match['player1'], match['player2'])

	async def connect(self):
		await self.accept()
		self.tournament_id = self.scope['url_route']['kwargs'].get('tournament_id')
		if not self.tournament_id:
			await self.send(text_data=json.dumps({'message': 'Tournament not found', 'status': 401}))
			await self.close()
		elif not self.scope['user']:
			await self.send(text_data=json.dumps({'message': 'User not authenticated', 'status': 401}))
			await self.close()
		try:
			self.tournament = await self.get_tournament(self.tournament_id)
			self.room_group_name = 'tournament_' + str(self.tournament_id)
			await self.get_or_create_dict(self.scope['profile'])
			self.profile = self.scope['profile']
			self.user = self.scope['user']
			await self.tournament_dict()
			await self.channel_layer.group_add(self.room_group_name, self.channel_name)
			alias_names = await self.get_alias_names()
			await get_channel_layer().group_send(
				self.room_group_name,
				{
					'type': 'broadcast_message',
					'message': alias_names,
					'm_type': 'joined'
				}
			)
			await self.check_tournament_state()
		except Tournament.DoesNotExist:
			await self.send(text_data=json.dumps({'message': 'Tournament not found', 'status': 401}))
			await self.close()



	async def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		m_type = text_data_json['type']
		if m_type == 'start_match':
			await self.start_point()
		elif m_type == 'won_user':
			await self.final_match(text_data_json)
		elif m_type == 'final_match_start':
			for match in tournament_dict[self.room_group_name]['matches']:
					await self.send_private_match_id(match['match_id'], match['player1'], match['player2'])


	async def final_match(self, text_data_json):
		winner_username = text_data_json['winner_name']
		loser_username = text_data_json['loser_name']
		winner_player_obj = await self.get_profile_object(winner_username)
		loser_player_obj = await self.get_profile_object(loser_username)
		alias_names = await self.get_alias_names()
		await asyncio.sleep(2.5)
		await self.send(text_data=json.dumps({
				'message': alias_names,
				'type': 'joined'
		}))
		if self.profile == winner_player_obj and  await self.get_tournament_round() != 2:
			tournament_dict[self.room_group_name]['losers'].append(loser_player_obj.alias_name)
			if tournament_dict[self.room_group_name]['semifinal1'] is None:
				tournament_dict[self.room_group_name]['semifinal1'] = self.profile
			elif tournament_dict[self.room_group_name]['semifinal2'] is None:
				tournament_dict[self.room_group_name]['semifinal2'] = self.profile
				await self.set_tournament_round()
				tournament_dict[self.room_group_name]['matches'].clear()
				new_match = await self.create_match(self.tournament, tournament_dict[self.room_group_name]['semifinal1'], tournament_dict[self.room_group_name]['semifinal2'])
				tournament_dict[self.room_group_name]['matches'].append(new_match)
				await asyncio.sleep(2.5)
				await get_channel_layer().group_send(
							self.room_group_name,
							{
								'type': 'winner_message',
								'm_type': 'winner_and_loser',
								'loser' : tournament_dict[self.room_group_name]['losers'],
							}
						)
		elif self.profile == winner_player_obj and await self.get_tournament_round() == 2:
			await self.set_champion()
			await self.change_tournament_state(StatusChoices.FINISHED.value)
			tournament_dict[self.room_group_name]['champion'] = self.profile
			await get_channel_layer().group_send(
					self.room_group_name,
					{
						'type': 'winner_message',
						'm_type': 'end_tournament',
						'loser' : tournament_dict[self.room_group_name]['losers'],
					}
				)

	#BAKICAM
	async def disconnect(self, code):
		if len(tournament_dict[self.room_group_name]['profiles']) == 1:
			tournament_dict.pop(self.room_group_name, None)
			await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
			await asyncio.sleep(2)
			if self.room_group_name not in tournament_dict:
				await self.set_alias_name()
				await self.delete_tournament()
		else:
			for p in tournament_dict[self.room_group_name]['profiles']:
				if p['profile'] == self.scope['profile']:
					tournament_dict[self.room_group_name]['profiles'].remove(p)
					alias_names = await self.get_alias_names()
					await get_channel_layer().group_send(
						self.room_group_name,
						{
							'type': 'broadcast_message',
							'message': alias_names,
							'm_type': 'joined'
						}
					)
					await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
					break
			await asyncio.sleep(2)
			for p in tournament_dict[self.room_group_name]['profiles']:
				if p['profile'] == self.scope['profile']:
					return
			tournament_player = await self.get_self_player_tournament()
			if tournament_player.creator == True:
				await self.set_tournament_creator()
			await self.delete_tournament_player(tournament_player)
			await self.set_alias_name()










	#Utils Function Get or DB set.
	async def get_or_create_dict(self, profile):
		if self.room_group_name in tournament_dict:
			if not any(p['profile'] == profile for p in tournament_dict[self.room_group_name]['profiles']):
				tournament_dict[self.room_group_name]['profiles'].append({'profile' : profile, 'alias_name': profile.alias_name})
		else:
			tournament_dict[self.room_group_name] = {
				'profiles' : [{'profile' :  profile, 'alias_name' : profile.alias_name}],
				'matches' : [],
				'semifinal1': None,
				'semifinal2': None,
				'champion': None,
				'losers': []
			}

	async def broadcast_message(self, event):
		m_type = event['m_type']
		message = event['message']

		await self.send(text_data=json.dumps({
			'type': m_type,
			'message': message
		}))

	async def winner_message(self, event):
		m_type = event['m_type']
		loser = event['loser']
		semifinal1 = tournament_dict[self.room_group_name]['semifinal1'].alias_name if tournament_dict[self.room_group_name]['semifinal1'] else None
		semifinal2 = tournament_dict[self.room_group_name]['semifinal2'].alias_name if tournament_dict[self.room_group_name]['semifinal2'] else None
		champion = tournament_dict[self.room_group_name]['champion'].alias_name if tournament_dict[self.room_group_name]['champion'] else None

		send_winners = [semifinal1, semifinal2, champion]

		await self.send(text_data=json.dumps({
			'type': m_type,
			'winner': send_winners,
			'loser': loser
		}))

	@database_sync_to_async
	def get_tournament(self, tournament_id):
		tournament = Tournament.objects.get(id=tournament_id)
		return tournament

	@database_sync_to_async
	def tournament_dict(self):
		print("self : ", tournament_dict[self.room_group_name])

	@database_sync_to_async
	def get_self_player_tournament(self):
		try:
			tournament_player = PlayerTournament.objects.get(player=self.scope['profile'], tournament=self.tournament)
		except PlayerTournament.DoesNotExist as e:
			print(f"Error: {e}", flush=True)
		return tournament_player

	@database_sync_to_async
	def set_tournament_creator(self):
		new_creator = None
		for p in tournament_dict[self.room_group_name]['profiles']:
				if p['profile'] != self.scope['profile']:
					new_creator = p['profile']
					break
		if new_creator:
			tournamnet_player = PlayerTournament.objects.get(player=new_creator, tournament=self.tournament)
			tournamnet_player.creator = True
			tournamnet_player.save()
			return True
		else:
			return False

	@database_sync_to_async
	def delete_tournament_player(self, tournament_player):
		tournament_player.delete()

	@database_sync_to_async
	def delete_tournament(self):
		self.tournament.delete()

	@database_sync_to_async
	def change_tournament_state(self, status):
		tournament = Tournament.objects.get(id=self.tournament_id)
		tournament.status = status
		tournament.save()

	@database_sync_to_async
	def get_profile_object(self, username):
		for profiles in tournament_dict[self.room_group_name]['profiles']:
			if profiles['profile'].user.username == username:
				return profiles['profile']
		return None

	async def get_alias_names(self):
		alias_names = []
		for player in tournament_dict[self.room_group_name]['profiles']:
			alias_names.append(player['alias_name'])
		return alias_names


	@database_sync_to_async
	def set_tournament_round(self):
		tournament = Tournament.objects.get(id=self.tournament_id)
		tournament.round += 1
		tournament.save()

	@database_sync_to_async
	def get_tournament_round(self):
		tournament = Tournament.objects.get(id=self.tournament_id)
		return tournament.round

	@database_sync_to_async
	def set_champion(self):
		self.profile.championships += 1
		self.profile.save()

	@database_sync_to_async
	def set_alias_name(self):
		self.profile.alias_name = ''
		self.profile.save()
