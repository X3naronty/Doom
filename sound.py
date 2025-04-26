from settings import *
import pygame

class Sound:
	def __init__(
			self,
			game,
			path = join("resources", "sound")
	):
		self.game = game
		pygame.mixer.init()
		self.gun_shot = pygame.mixer.Sound(join(path, "shotgun.wav"))
		self.npc_pain = pygame.mixer.Sound(join(path, "npc_pain.wav"))
		self.npc_death = pygame.mixer.Sound(join(path, "npc_death.wav"))
		self.npc_shot = pygame.mixer.Sound(join(path, "npc_attack.wav"))
		self.player_pain = pygame.mixer.Sound(join(path, "player_pain.wav"))
		self.theme = pygame.mixer.music.load(join(path,"theme.mp3"))
