from sprite_object import AnimatedSprite, SpriteObject
from os.path import join
from npc import NPC

class ObjectHandler:
	def __init__(self, game):
		self.game = game
		self.sprite_list = []
		self.npc_list = []
		self.npc_sprite_path = join("resources", "sprites", "npc")
		self.static_sprite_path = join("resources", "sprites", "static_sprites")
		self.animated_sprite_path = join("resources", "sprites", "animated_sprites")
		add_sprite = self.add_sprite
		add_npc = self.add_npc

		add_sprite(SpriteObject(game))
		add_sprite(AnimatedSprite(game))
		
		add_npc(NPC(game))
		
	def update(self):
		[sprite.update() for sprite in self.sprite_list]
		[npc.update() for npc in self.npc_list]
	
	def add_npc(self, npc):
		self.npc_list.append(npc)
		
	def add_sprite(self, sprite):
		self.sprite_list.append(sprite)
		
