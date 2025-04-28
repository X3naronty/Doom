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
		self.health = 100
		self.rel = 0
		self.health_recovery_delay = 700
		self.time_prev = pygame.time.get_ticks()
		
	def recover_health(self):
		if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
			self.health += 1
			
	def check_health_recovery_delay(self):
		time_now = pygame.time.get_ticks()
		if time_now - self.time_prev > self.health_recovery_delay:
			self.time_prev = time_now
			return True
		
	def check_game_over(self):
		if self.health < 1:
			self.game.object_renderer.game_over()
			pygame.display.flip()
			pygame.time.delay(1500)
			self.game.assign_game_entities()
			
	def check_win(self):
		if not any([npc.alive or npc.is_animating for npc in self.game.object_handler.npc_list]):
			self.game.object_renderer.player_win()
			pygame.display.flip()
			pygame.time.delay(1500)
			self.game.assign_game_entities()
		
	def get_damage(self, damage):
		self.health -= damage
		self.game.object_renderer.player_damage()
		self.game.sound.player_pain.play()
		self.check_game_over()

	
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

		scale = PLAYER_SIZE / self.game.delta_time
		if self.is_not_collided(int(self.x + dx * scale), int(self.y)):
			self.x += dx
		if self.is_not_collided(int(self.x), int(self.y + dy * scale)):
			self.y += dy
		
		# if keys[pygame.K_LEFT]:
		# 	self.angle += -PLAYER_ROT_SPEED * self.game.delta_time
		# if keys[pygame.K_RIGHT]:
		# 	self.angle += PLAYER_ROT_SPEED * self.game.delta_time

	def is_not_collided(self, x, y):
		return (x, y) not in self.game.map.objects

	def draw(self):
		# pygame.draw.line(self.game.window, "yellow", (self.x * 100, self.y * 100), (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + WIDTH * math.sin(self.angle)), 2)	
		pygame.draw.circle(self.game.window, "green", (self.x * 100, self.y * 100), 15)
	
	def handle_mouse(self):
		mx, my = pygame.mouse.get_pos()
		if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
			pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
		self.rel = pygame.mouse.get_rel()[0]
		self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
		self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
		self.angle %= math.tau

	def update(self):
		self.movement()
		self.handle_mouse()
		self.raycasting.update()
		self.recover_health()
		self.check_win()
	
	@property 
	def pos(self):
		return self.x, self.y

	@property 
	def map_pos(self):
		return int(self.x), int(self.y)

