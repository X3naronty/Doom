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
