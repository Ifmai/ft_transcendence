from enum import Enum

class State(Enum):
	PLAYED = "PLY"
	UNPLAYED = "UPL"

	@classmethod
	def choices(cls):
		return [(choice.value, choice.name) for choice in cls]

class Status(Enum):
		ONLINE = 'ON'
		OFFLINE = 'OF'
		INGAME = 'IG'

class StatusChoices(Enum):
	PENDING = 'PN'
	IN_PROGRESS = 'PG'
	FINISHED = 'FN'

	@classmethod
	def choices(cls):
		return [(choice.value, choice.name) for choice in cls]

TOURNAMENT_SIZE = 4