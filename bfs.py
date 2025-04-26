from collections import deque

class BFS:
	def __init__(self, game):
		self.game = game
		self.map = game.map.mini_map
		self.obstacles = game.map.objects
		self.ways = [
			(-1, -1),
			(-1, 0),
			(-1, 1),
			(0, 1),
			(1, 1),
			(1, 0),
			(1, -1),
			(0, -1)
		]
		self.graph = self.create_graph()
		
	def create_graph(self):
		graph = {}
		
		for i, row in enumerate(self.map):
			for j, val in enumerate(row):
				if not val:
					graph[(j, i)] = [
						(j + dx, i + dy) for (dx, dy) in self.ways if (j + dx, i + dy) not in self.obstacles
					]
		return graph
	
	def get_next_step(self, start, end):
		visited = self.search(start, end)
		path = [end]
		step = visited.get(end, start)
		
		while step != start and step:
			path.append(step)
			step = visited[step]
		return path[-1]
	
	def search(self, start, end):
		used = {start: None}
		queue = deque([start])
		
		while(queue):
			cur = queue.popleft()

			if cur == end:
				break
			
			for node in self.graph[cur]:
				if node not in used and node not in self.game.object_handler.npc_positions:
					used[node] = cur 
					queue.append(node)

		return used	
	
	



		

		
		

		