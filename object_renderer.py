from settings import * 
import pygame

class ObjectRenderer:
	def __init__(self, game):
		self.game = game
		self.window = game.window
		self.wall_textures = self.load_wall_textures()
		self.sky_image = self.get_texture(SKY_IMAGE_PATH, (WIDTH, HALF_HEIGHT))
		self.blood_screen = self.get_texture(join("resources", "textures", "blood_screen.png"), RES)
		self.sky_offset = 0
		
		self.game_over_screen = self.get_texture(join("resources", "textures", "game_over.png"), RES)
		self.game_win_screen = self.get_texture(join("resources", "textures", "win.png"), RES)
		
		self.digit_size = 90
		self.digit_images = [self.get_texture(join("resources", "textures", "digits", f"{i}.png"), [self.digit_size] * 2) for i in range(11)]
		self.digits = dict(zip(map(str, range(11)), self.digit_images))
		
	def player_win(self):
		self.window.blit(self.game_win_screen, (0, 0))	
	
	def player_damage(self):
		self.window.blit(self.blood_screen, (0, 0))
		
	def game_over(self):
		self.window.blit(self.game_over_screen, (0, 0))
		
	def draw(self):
		self.draw_background()
		self.render_game_objects()
		self.draw_player_health()

	def draw_background(self):
		
		self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
		self.window.blit(self.sky_image, (-self.sky_offset, 0))
		self.window.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
		
		# floor
		pygame.draw.rect(self.window, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

	def draw_player_health(self):
		health = str(self.game.player.health)	
		for i, char in enumerate(health):
			self.window.blit(self.digits[char], (i * self.digit_size, 0))
		self.window.blit(self.digits["10"], ((i + 1) * self.digit_size, 0))

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
			
		