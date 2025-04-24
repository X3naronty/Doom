from settings import * 
import pygame

class ObjectRenderer:
	def __init__(self, game):
		self.game = game
		self.window = game.window
		self.wall_textures = self.load_wall_textures()
		self.sky_image = self.get_texture(SKY_IMAGE_PATH, (WIDTH, HALF_HEIGHT))
		self.sky_offset = 0
		
	def draw(self):
		self.draw_background()
		self.render_game_objects()

	def draw_background(self):
		self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
		self.window.blit(self.sky_image, (-self.sky_offset, 0))
		self.window.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
		
		# floor
		pygame.draw.rect(self.window, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
		

	def render_game_objects(self):
		list_objects = sorted(self.game.player.raycasting.objects_to_render, key = lambda t:t[0], reverse = True)
		for depth, image, pos in list_objects:
			self.window.blit(image, pos)
	
	@staticmethod
	def get_texture(path, res = (TEXTURE_SIZE, TEXTURE_SIZE)):
		texture = pygame.image.load(path).convert_alpha()
		return pygame.transform.scale(texture, res)
	
	def load_wall_textures(self):
		textures = {}
		for i in range(1, TEXTURE_WALL_NUM + 1):
			textures[i] = ObjectRenderer.get_texture(join(TEXTURE_WALL_PATH, f"{i}.png"))
		return textures
			
		