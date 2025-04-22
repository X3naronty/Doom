import math

import pygame

from settings import *

from raycasting import Raycasting

class Player:
	def __init__(self, game):
		self.game = game
		self.x, self.y = PLAYER_POS
		self.angle = PLAYER_ANGLE	
		self.raycasting = Raycasting(self)
	
	def movement(self):
		a_cos = math.cos(self.angle)
		a_sin = math.sin(self.angle)
		dx, dy = 0, 0
		speed = PLAYER_SPEED * self.game.delta_time 
		speed_sin = speed * a_sin
		speed_cos = speed * a_cos

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			dx += speed_cos
			dy += speed_sin
		elif keys[pygame.K_s]:
			dx += -speed_cos
			dy += -speed_sin
		elif keys[pygame.K_d]:
			dx += -speed_sin
			dy += speed_cos
		elif keys[pygame.K_a]:
			dx += speed_sin
			dy += -speed_cos

		if self.is_not_collided(int(self.x + dx), int(self.y)):
			self.x += dx
		if self.is_not_collided(int(self.x), int(self.y + dy)):
			self.y += dy
		
		if keys[pygame.K_LEFT]:
			self.angle += -PLAYER_ROT_SPEED * self.game.delta_time
		if keys[pygame.K_RIGHT]:
			self.angle += PLAYER_ROT_SPEED * self.game.delta_time
		self.angle %= math.tau

	def is_not_collided(self, x, y):
		return (x, y) not in self.game.map.objects

	def draw(self):
		# pygame.draw.line(self.game.window, "yellow", (self.x * 100, self.y * 100), (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + WIDTH * math.sin(self.angle)), 2)	
		pygame.draw.circle(self.game.window, "green", (self.x * 100, self.y * 100), 15)

	def update(self):
		self.movement()
		self.raycasting.update()
	
	@property 
	def pos(self):
		return self.x, self.y

	@property 
	def map_pos(self):
		return int(self.x), int(self.y)

