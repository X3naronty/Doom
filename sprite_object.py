import math
from os.path import join, isfile

import pygame

from settings import *
from os import listdir

from collections import deque


class SpriteObject:
	def __init__(self, game, 
			  		path = join("resources", "sprites", "static_sprites"), 
					pos = (6, 6),
					scale = 1.0,
					vertical_shift = 0.2
				):
		self.game = game
		self.x, self.y = pos

		path = join(path, listdir(path)[0])
		self.image = pygame.image.load(path).convert_alpha()

		self.IMAGE_WIDTH = self.image.get_width()
		self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
		self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
		self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
		self.sprite_half_width = 0
		self.SPRITE_VERTICAL_SHIFT = vertical_shift
		self.SPRITE_SCALE = scale
		
	def render_sprite(self):
		dx = self.x - self.game.player.x 
		dy = self.y - self.game.player.y
		self.dx, self.dy = dx, dy
		self.theta = math.atan2(dy, dx)

		delta = self.theta - self.game.player.angle
		if delta < -math.pi:
			delta += math.tau
		elif delta > math.pi:
			delta -= math.tau

		delta_rays = delta / DELTA_ANGLE
		self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE	
		
		self.norm_dist = math.hypot(dx, dy) 
		if -self.IMAGE_HALF_WIDTH < self.screen_x < WIDTH + self.IMAGE_HALF_WIDTH and self.norm_dist > 0.5:
			self.get_sprite_projection()
	
	def get_sprite_projection(self):
		proj_height = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
		proj_width = proj_height * self.IMAGE_RATIO
		
		image = pygame.transform.scale(self.image, (proj_width, proj_height))
		self.sprite_half_width = proj_width // 2
		vertical_shift = proj_height * self.SPRITE_VERTICAL_SHIFT	
		pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + vertical_shift
		self.game.player.raycasting.objects_to_render.append((self.norm_dist, image, pos))
		
	
	def update(self):
		self.render_sprite()
	

class AnimatedSprite(SpriteObject):
	def __init__(   self, game, 
					path = join("resources", "sprites", "animated_sprites", "red_light"), 
					pos = (10, 2),
					scale = 1.0,
					vertical_shift = 0.2,
					animation_time = 120
				):
		super().__init__(game, path, pos, scale, vertical_shift)
		self.animation_time = animation_time
		self.images = self.get_images(path)
		self.animation_time_prev = pygame.time.get_ticks()
		self.animation_trigger = False
	
	def update(self):
		super().update()
		self.check_animation_time()
		self.animate(self.images)
	
	def animate(self, images):
		if self.animation_trigger:
			images.rotate(-1)
			self.image = images[0]
	
	def check_animation_time(self):
		self.animation_trigger = False
		time_now = pygame.time.get_ticks()
		if time_now - self.animation_time_prev > self.animation_time:
			self.animation_time_prev = time_now
			self.animation_trigger = True
	
	def get_images(self, path):
		images = deque()
		for image_name in listdir(path):
			image_path = join(path, image_name)
			if isfile(image_path):
				img = pygame.image.load(image_path).convert_alpha()
				images.append(img)
		return images
		
