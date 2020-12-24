from timeit import default_timer as timer
import re

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
		return  "Grid size %d" % (len(self.grid))

	def __repr__(self):
		return  str(self)

	def __getitem__(self, coord):
		if coord not in self.grid:
			self.grid[coord] = HexCell(coord)
		return self.grid[coord]

	def neighbors(self, curr):
		for neighbor in self.neighbor_coords(curr.coord):
			yield self[neighbor]

	def neighbor_coords(self, coord):
		for direction in DIRECTIONS.values():
			yield self.get_next_coord(coord, direction)

	def get_next_coord(self, coord, direction):
		return (coord[0] + direction[0], coord[1] + direction[1])

	def get_next(self, curr, direction, ensure_neighbors = False):
		coord = (curr.x + direction[0], curr.z + direction[1])
		curr = self[coord]
		if ensure_neighbors:
			self.neighbors(curr)
		return curr

	def items(self):
		return self.grid.items()

DIRECTIONS = {
	"e": (1,0),
	"se": (1,-1),
	"sw": (0,-1),
	"w": (-1,0),
	"nw": (-1,1),
	"ne": (0,1),
}

start = timer()
file = open('input.txt')

grid = HexGrid()
pattern = r"(se|sw|ne|nw|w|e)";
for line in file.readlines():
	curr = grid[(0,0)]
	for val in re.findall(pattern, line):
		direction = DIRECTIONS[val]
		curr = grid.get_next(curr, direction)
	curr.flip()

result = 0
for (coord, tile) in grid.items():
	if tile.val == 1:
		# print tile
		result += 1


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)






