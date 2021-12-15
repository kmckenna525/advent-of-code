from timeit import default_timer as timer
import re
from queue import PriorityQueue

start = timer()
file = open('input.txt')

def wrap(val):
	return ((val - 1) % 9) + 1


class Map2D:
	def __init__(self, multiplier = 1):
		self.map = {}
		self.width = 0
		self.height = 0
		self.multiplier = multiplier


	def __str__(self):
		return str(self.map)


	def __repr__(self):
		return str(self.map)


	def __getitem__(self, coord):
		coord, rowoffset, coloffset = self.unpack_virtual_coord(coord)
		return self.remap_value(coord, self.map[coord], rowoffset, coloffset)


	def __setitem__(self, coord, value):
		self.add_coord(coord, value)


	@property
	def virtual_height(self):
		return self.height * self.multiplier

	@property
	def virtual_width(self):
		return self.width * self.multiplier


	def unpack_virtual_coord(self, coord):
		row = coord.row
		rowoffset = 0
		col = coord.col
		coloffset = 0
		if row >= self.height:
			rowoffset = int(row / self.height)
			row = row % self.height;
		if col >= self.height:
			coloffset = int(col / self.width)
			col = col % self.width;
		return (Coord(row, col), rowoffset, coloffset)


	@property
	def coords(self):
		for i in range(0, self.virtual_height):
			for j in range(0, self.virtual_width):
				yield Coord(i,j)


	def add_coord(self, coord, value):
		self.map[coord] = value
		if coord.row >= self.height:
			self.height = coord.row + 1
		if coord.col >= self.width:
			self.width = coord.col + 1


	def is_valid(self, coord):
		return (
			coord.row >= 0 and 
			coord.row < self.virtual_height and
			coord.col >= 0 and 
			coord.col < self.virtual_width
		)


	def valid_neighbors(self, coord):
		for neighbor in coord.neighbors:
			if self.is_valid(neighbor):
				yield neighbor


	def remap_value(self, coord, val, rowoffset, coloffset):
		return wrap(val + rowoffset + coloffset)


	def debug(self):
		for i in range(0, self.virtual_height):
			s = ""
			for j in range(0, self.virtual_width):
				if j % self.width == 0:
					s += " "
				s += str(self[Coord(i,j)])
			if i % self.height == 0:
				print ""
			print s
		print ""


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




class Coord:
	def __init__(self, row, col):
		self.row = row
		self.col = col

	def __str__(self):
		return  "%d,%d" % (self.row, self.col)

	def __repr__(self):
		return  "%d,%d" % (self.row, self.col)

	def __hash__(self):
		 return hash((self.row, self.col))

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.row == other.row and
			self.col == other.col
		)

	@property
	def right(self):
		return Coord(self.row, self.col + 1)

	@property
	def left(self):
		return Coord(self.row, self.col - 1)

	@property
	def up(self):
		return Coord(self.row - 1, self.col)

	@property
	def down(self):
		return Coord(self.row + 1, self.col)

	@property
	def neighbors(self):
		yield Coord(self.row+1, self.col)
		yield Coord(self.row-1, self.col)
		yield Coord(self.row, self.col+1)
		yield Coord(self.row, self.col-1)

memo = {}
def heuristic(riskmap, coord, target):
	# calculate diagonal path cost
	if coord in memo:
		return memo[coord]

	if coord == target:
		return 0

	total_risk = float("inf")
	if riskmap.is_valid(coord.right):
		total_risk = riskmap[coord.right] + heuristic(riskmap, coord.right, target)

	if riskmap.is_valid(coord.down):
		total_risk = riskmap[coord.down] + heuristic(riskmap, coord.down, target)

	memo[coord] = total_risk
	return total_risk

		
riskmap = Map2D(5)
row = 0
for line in file.readlines():
	col = 0
	for val in line.strip():
		riskmap.add_coord(Coord(row, col), int(val))
		col += 1
	row += 1
# riskmap.debug()

parent = {} # coord: best parent
opencoords = {} # coord: fscore if currently in queue
opencoords[Coord(0,0)] = 0
unseen = PriorityQueue() # (fscore, coord)
unseen.put((0, Coord(0,0))) 
gscore = DefaultValueMap(float("inf"))
gscore[Coord(0,0)] = 0

target = Coord(riskmap.virtual_height - 1, riskmap.virtual_width - 1)
result = float("inf")
while not unseen.empty():
	fscore, coord = unseen.get()
	if coord not in opencoords: # we probably found a better path
		continue
	if coord == target:
		final = gscore[coord]
		memo.clear()
		while coord is not None:
			memo[coord] = final - gscore[coord]
			coord = parent[coord] if coord in parent else None
		continue
	opencoords.pop(coord)

	for neighbor in riskmap.valid_neighbors(coord):
		neighbor_gscore = gscore[coord] + riskmap[neighbor]
		if neighbor_gscore < gscore[neighbor]:
			parent[neighbor] = coord
			gscore[neighbor] = neighbor_gscore
			neighbor_fscore = neighbor_gscore + heuristic(riskmap, neighbor, target)
			opencoords[neighbor] = neighbor_fscore
			unseen.put((neighbor_fscore, neighbor))
result = gscore[target]

# coord = target
# while coord is not None:
# 	print coord, riskmap[coord]
# 	coord = parent[coord] if coord in parent else None


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)