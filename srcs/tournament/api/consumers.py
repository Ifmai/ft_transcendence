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
		if len(tournament_dict[self.room_group_name]['profiles']) == 4:
			player1 = tournament_dict[self.room_group_name]['profiles'][0]['profile']
			player2 = tournament_dict[self.room_group_name]['profiles'][3]['profile']
			player3 = tournament_dict[self.room_group_name]['profiles'][1]['profile']
			player4 = tournament_dict[self.room_group_name]['profiles'][2]['profile']

			match_info1 = await self.create_match(self.tournament, player1, player2)
			tournament_dict[self.room_group_name]['matches'].append(match_info1)
			match_info2 = await self.create_match(self.tournament, player3, player4)
			tournament_dict[self.room_group_name]['matches'].append(match_info2)
			self.change_tournament_state()
			await self.tournament_dict()

	async def start_point(self):
		while True:
			if self.tournament.status != StatusChoices.PENDING.value:
				break
			if len(tournament_dict[self.room_group_name]['matches']) == 2:
				for match in tournament_dict[self.room_group_name]['matches']:
					await self.send_private_match_id(match['match_id'], match['player1'], match['player2'])
				break
			await asyncio.sleep(0.1)  # Döngü içinde bekleme süresi

	async def connect(self):
		await self.accept()
		tournament_id = self.scope['url_route']['kwargs'].get('tournament_id')
		if not tournament_id:
			await self.send(text_data=json.dumps({'message': 'Torunament not found', 'status': 401}))
			await self.close()
		elif not self.scope['user']:
			await self.send(text_data=json.dumps({'message': 'User not authenticated', 'status': 401}))
			await self.close()
		try:
			self.tournament = await self.get_tournament(tournament_id)
			self.room_group_name = 'tournament_' + str(tournament_id)
			await self.get_or_create_dict(self.scope['profile'])
			self.profile = self.scope['profile']
			self.user = self.scope['user']
			await self.tournament_dict()
			await self.channel_layer.group_add(self.room_group_name, self.channel_name)
			join_message = f"{self.scope['profile'].alias_name} has joined the tournament!"
			await get_channel_layer().group_send(
				self.room_group_name,
				{
					'type': 'broadcast_message',
					'message': join_message,
					'm_type': 'joined'
				}
			)
			for player in tournament_dict[self.room_group_name]['profiles']:
				if player['alias_name'] != self.scope['profile'].alias_name:
					await self.send(text_data=json.dumps({
						'type': 'joined',
						'message': f"{player['alias_name']} has joined the tournament!"
					}))
			await self.check_tournament_state()
		except Tournament.DoesNotExist:
			await self.send(text_data=json.dumps({'message': 'Tournament not found', 'status': 401}))
			await self.close()

	async def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		print("Text Data json : ", text_data_json)
		m_type = text_data_json['type']
		print("m_type", m_type)
		if m_type == 'init':
			print("geldim")
			asyncio.create_task(self.start_point())
		return await super().receive(text_data, bytes_data)

	async def disconnect(self, code):
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
		tournament_player = await self.get_self_player_tournament()
		if len(tournament_dict[self.room_group_name]['profiles']) == 1:
			tournament_dict.pop(self.room_group_name, None)
			asyncio.sleep(5)
			if self.room_group_name not in tournament_dict:
				await self.delete_tournament()
		elif tournament_player:
			for p in tournament_dict[self.room_group_name]['profiles']:
				if p['profile'] == self.scope['profile']:
					tournament_dict[self.room_group_name]['profiles'].remove(p)
					await self.tournament_dict()
					break
			if tournament_player.creator == True:
				await self.set_tournament_creator()
			asyncio.sleep(2)
			if not any(p['profile'] != self.scope['profile'] for p in tournament_dict[self.room_group_name]['profiles']):
				await self.delete_tournament_player(tournament_player)


	#Utils Function Get or DB set.
	async def get_or_create_dict(self, profile):
		if self.room_group_name in tournament_dict:
			if not any(p['profile'] == profile for p in tournament_dict[self.room_group_name]['profiles']):
				tournament_dict[self.room_group_name]['profiles'].append({'profile' : profile, 'alias_name': profile.alias_name})
		else:
			tournament_dict[self.room_group_name] = {
				'profiles' : [{'profile' :  profile, 'alias_name' : profile.alias_name}],
				'matches' : []
			}

	async def broadcast_message(self, event):
		message = event['message']
		m_type = event['m_type']
        
		await self.send(text_data=json.dumps({
			'type': m_type,
			'message': message
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
		tournament_player = PlayerTournament.objects.get(player=self.scope['profile'], tournament=self.tournament)
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
	def change_tournament_state(self):
		self.tournament.status = StatusChoices.IN_PROGRESS
		self.tournament.save()
