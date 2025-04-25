import pygame 

_ = False	
mini_map = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, 1],
	[1, _, _, _, _, _, 2, _, _, _, _, _, 4, 4, _, 1],
	[1, _, 5, 5, _, _, 2, 2, _, _, _, _, 4, _, _, 1],
	[1, _, _, 5, _, _, _, _, _, _, _, _, 4, _, _, 1],
	[1, _, _, 5, _, _, _, _, 3, 3, _, _, 4, 4, _, 1],
	[1, _, 5, 5, _, _, _, _, _, 3, _, _, _, _, _, 1],
	[1, _, _, _, _, _, _, _, _, 3, _, _, _, _, _, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:
	def __init__(self, game):
		self.game = game
		self.mini_map = mini_map
		self.objects = Map.get_objects(self)
	
	def draw(self):
		[
			pygame.draw.rect(self.game.window, "darkgrey", (pos[0] * 100, pos[1] * 100, 100, 100), 3)
   			for pos in self.objects
		]

	@staticmethod
	def get_objects(map):
		objects = {}

		for i, row in enumerate(map.mini_map):
			for index, value in enumerate(row):
				if value: objects[(index, i)] = value
		# print(objects)
		return objects



