from timeit import default_timer as timer
from queue import PriorityQueue

start = timer()
file = open('input.txt')

def can_move(src, dst):
	if dst <= src:
		return True
	return ord(dst) - ord(src) == 1

class Grid:
	def __init__(self):
		self.grid = {}
		self.height = 0
		self.width = 0
		self.start = None
		self.target = None

	def debug(self):
		for y in range(self.height):
			s = ""
			for x in range(self.width):
				s += self.get(x, y)
			print s

	def set(self, x, y, val):
		if x >= self.width:
			self.width = x + 1
		if y >= self.height:
			self.height = y + 1
		if val == "S":
			self.start = (x,y)
			self.grid[(x,y)] = "a"
		elif val == "E":
			self.target = (x,y)
			self.grid[(x,y)] = "z"
		else:
			self.grid[(x,y)] = val

	def get(self, x, y):
		return self.grid[(x,y)]

	def get_coord(self, coord):
		return self.grid[coord]

	def neighbors(self, coord):
		(x,y) = coord
		if x > 0:
			yield (x - 1, y)
		if y > 0:
			yield (x, y - 1)
		if x < self.width - 1:
			yield (x + 1, y)
		if y < self.height - 1:
			yield (x, y + 1)

	def valid_neighbors(self, coord):
		val = self.get_coord(coord)
		for neighbor in self.neighbors(coord):
			if can_move(val, self.get_coord(neighbor)):
				yield neighbor

	def get_possible_starts(self):
		for y in range(self.height):
			for x in range(self.width):
				if self.get(x,y) == "a":
					yield (x,y)


class DefaultValueMap:
	def __init__(self, default = None):
		self.map = {}
		self.default = default

	def __str__(self):
		return str(self.map)


	def __repr__(self):
		return str(self.map)


	def __getitem__(self, key):
		if key not in self.map:
			return self.default
		return self.map[key]


	def __setitem__(self, key, value):
		self.map[key] = value


def heuristic(coord, grid):
	return (grid.target[0] - coord[0]) + (grid.target[1] - coord[1])


grid = Grid()
result = 0
x = 0
y = 0
for line in file.read().split("\n"):
	for c in line:
		grid.set(x, y, c)
		x += 1
	x = 0
	y += 1

file.close()

# do some A* as a function
def a_star(grid, origin):
	parent = {} # coord: best parent
	opencoords = {} # coord: fscore if currently in queue
	opencoords[origin] = 0
	unseen = PriorityQueue() # (fscore, coord)
	unseen.put((0, origin)) 
	gscore = DefaultValueMap(float("inf"))
	gscore[origin] = 0

	target = grid.target
	result = float("inf")
	while not unseen.empty():
		fscore, coord = unseen.get()
		if coord not in opencoords: # we probably found a better path
			continue
		if coord == target:
			result = gscore[coord]
			break
		opencoords.pop(coord)

		for neighbor in grid.valid_neighbors(coord):
			neighbor_gscore = gscore[coord] + 1
			if neighbor_gscore < gscore[neighbor]:
				parent[neighbor] = coord
				gscore[neighbor] = neighbor_gscore
				neighbor_fscore = neighbor_gscore + heuristic(neighbor, grid)
				opencoords[neighbor] = neighbor_fscore
				unseen.put((neighbor_fscore, neighbor))
	result = gscore[target]
	return result

# do all the A*s
result = float("inf")
for coord in grid.get_possible_starts():
	path = a_star(grid, coord)
	if path < result:
		result = path


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)