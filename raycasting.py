import math
from settings import *
import pygame

class Raycasting:
	def __init__(self, player):
		self.player = player
		
	def ray_cast(self):
		ox, oy = self.player.pos
		x_map, y_map = self.player.map_pos

		ray_angle = self.player.angle - HALF_FOV + 0.001
		for ray in range(NUM_RAYS):
			cos_a = math.cos(ray_angle)
			sin_a = math.sin(ray_angle)

			# verticals
			x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
			depth_vert = (x_vert - ox) / cos_a
			y_vert = oy + depth_vert * sin_a
			
			delta_depth = dx / cos_a
			dy = delta_depth * sin_a

			for i in range(MAX_DEPTH):
				tile_vert = int(x_vert), int(y_vert)	
				if tile_vert in self.player.game.map.objects:
					break
				x_vert += dx 
				y_vert += dy
				depth_vert += delta_depth
				

			# horizontals

			y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1) 
			depth_hor = (y_hor - oy) / sin_a
			x_hor = ox + depth_hor * cos_a

			delta_depth = dy / sin_a
			dx = delta_depth * cos_a
			
			for i in range(MAX_DEPTH):
				tile_hor = int(x_hor), int(y_hor)
				if tile_hor in self.player.game.map.objects:
					break
				x_hor += dx
				y_hor += dy
				depth_hor += delta_depth

			depth = min(depth_hor, depth_vert)
			
			# draw for debug
			# pygame.draw.line(self.player.game.window, "yellow" (100 * ox, 100 * oy),
			# 		(100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

			depth *= math.cos(self.player.angle - ray_angle)	
			proj_height = SCREEN_DIST / (depth + 0.0001)
			color = [255 / (1 + depth ** 5 * 0.00002)] * 3	
			pygame.draw.rect(self.player.game.window, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

			ray_angle += DELTA_ANGLE


	def update(self):
		self.ray_cast()
	
	
	