from sprite_object import SpriteObject, AnimatedSprite
from random import randint, random, choice
from os.path import join
from settings import *

class NPC(AnimatedSprite):
	def __init__(
			self,
			game, 
			path = join("resources", "sprites", "npc", "soldier", "idle"),
			pos = (4, 1.5),
			scale = 0.6,
			shift = 0.38,
			animation_time = 180
	):
		super().__init__(game, path, pos, scale, shift, animation_time)
		self.sprites = {} 
		self.sprites["attack"] = self.get_images(join(path, "..", "attack"))
		self.sprites["death"] = self.get_images(join(path, "..", "death"))
		self.sprites["idle"] = self.get_images(join(path, "..", "idle"))
		self.sprites["pain"] = self.get_images(join(path, "..", "pain"))
		self.sprites["walk"] = self.get_images(join(path, "..", "walk"))
		
		self.attack_dist = randint(3, 6)
		self.speed = 0.03
		self.size = 10
		self.health = 100
		self.attack_damage = 10
		self.accuracy = 0.15
		self.alive = True
		self.pain = False

		self.images = self.sprites["idle"]

		self.animation_count = 0
		
	def update(self):
		self.check_animation_time()
		self.run_logic()
		self.render_sprite()
		
	
	# def animate_pain():
		
		
	
	def check_hit(self):
		if self.game.weapon.shot and HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
			self.pain = True
			self.game.weapon.shot = False
		else: self.pain = False	
		return self.pain
	
	def run_logic(self):
		if self.alive: 
			if self.animation_count == len(self.images): 
				self.images = self.sprites["idle"]
				print(1)
			if self.check_hit():
				self.animation_count = 0
				self.images = self.sprites["death"]
				# print(2)
			self.animate()
			if self.animation_trigger: self.animation_count = (self.animation_count + 1) % len(self.images) + 1
			


		

