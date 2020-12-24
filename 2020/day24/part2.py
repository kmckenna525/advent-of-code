from timeit import default_timer as timer
import re

ITERATIONS = 100
DIRECTIONS = {
	"e": (1,0),
	"se": (1,-1),
	"sw": (0,-1),
	"w": (-1,0),
	"nw": (-1,1),
	"ne": (0,1),
}

class HexCell:
	def __init__(self, coord):
		self.coord = coord
		self.val = 0

	def __str__(self):
		return  "(%d,%d) %d" % (self.x, self.z, self.val)

	def __repr__(self):
		return  str(self)

	@property
	def x(self):
		return self.coord[0]

	@property
	def y(self):
		return - self.x - self.z

	@property
	def z(self):
		return self.coord[1]

	def flip(self):
		self.val = 1 if self.val == 0 else 0

class HexGrid:
	def __init__(self):
		self.grid = {}

	def __str__(self):
		return  str(list(self.values()))

	def __repr__(self):
		return  str(self)

	def __getitem__(self, coord):
		return self.get(coord)

	def get(self, coord, ensure = True):
		if coord not in self.grid:
			if not ensure:
				return None
			self.grid[coord] = HexCell(coord)
		return self.grid[coord]

	def neighbors(self, curr, ensure = True):
		for neighbor in self.neighbor_coords(curr.coord):
			yield self.get(neighbor, ensure)

	def neighbor_coords(self, coord):
		for direction in DIRECTIONS.values():
			yield self.get_next_coord(coord, direction)

	def get_next_coord(self, coord, direction):
		return (coord[0] + direction[0], coord[1] + direction[1])

	def get_next(self, curr, direction, ensure_neighbors = True):
		coord = (curr.x + direction[0], curr.z + direction[1])
		curr = self.get(coord, ensure_neighbors)
		if ensure_neighbors:
			for x in self.neighbors(curr, ensure_neighbors):
				pass
		return curr

	def items(self):
		return self.grid.items()

	def values(self):
		return self.grid.values()



start = timer()
file = open('input.txt')

grid = HexGrid()
grid.get((0,0), True)
grid.neighbors(grid[(0,0)], True)
pattern = r"(se|sw|ne|nw|w|e)";
for line in file.readlines():
	curr = grid[(0,0)]
	for val in re.findall(pattern, line):
		direction = DIRECTIONS[val]
		curr = grid.get_next(curr, direction, True)
	curr.flip()

def count(tiles):
	total = 0
	for tile in tiles:
		if tile is not None and tile.val == 1:
			# print tile
			total += 1
	return total

def run_game():
	to_flip = []
	for tile in grid.values():
		total = count(grid.neighbors(tile)) 
		if tile.val == 1:
			# 0 or more than 2 black tiles
			if total == 0 or total > 2:
				to_flip.append(tile)
	 	else:
			# 2 black tiles
			if total == 2:
				to_flip.append(tile)
	for tile in to_flip:
		tile.flip()
		grid.neighbors(tile, True) # make sure neighbors exist for flipped tiles

# print (list(grid.neighbors(grid[(0,-3)])))

for i in range(ITERATIONS):
	# print "Iteration %d" % (i + 1)
	run_game()
	# print count(grid.values())

result = count(grid.values())
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)






