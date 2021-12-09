from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')


class CaveMap:
	def __init__(self):
		self.heightmap = {}
		self.basins = None
		self.basinmap = None
		self.lowpoints = None
		self.width = 0
		self.height = 0

	def __str__(self):
		return str(self.map)

	def __repr__(self):
		return str(self.map)

	@property
	def coords(self):
		for i in range(0, self.height):
			for j in range(0, self.width):
				yield Coord(i,j)

	def add_coord(self, coord, value):
		self.heightmap[coord] = value
		if coord.row >= self.height:
			self.height = coord.row + 1
		if coord.col >= self.width:
			self.width = coord.col + 1

	def initialize_low_points(self):
		self.lowpoints = []
		for coord in self.coords:
			if self.is_low_point(coord):
				self.lowpoints.append(coord)

	def initialize_basins(self):
		self.basins = []
		self.basinmap = {}
		for coord in self.lowpoints:
			if coord in self.basinmap:
				continue
			self.basins.append(self.basinize(coord, self.basinmap))


	def basinize(self, coord, basinmap):
		basin = set()
		pending = set()
		pending.add(coord)

		while len(pending) > 0:
			coord = pending.pop()
			if self.heightmap[coord] == 9:
				continue
			basin.add(coord)
			basinmap[coord] = basin
			for neighbor in self.valid_neighbors(coord):
				if neighbor not in basin:
					pending.add(neighbor)

		return basin



	def is_valid(self, coord):
		return (
			coord.row >= 0 and 
			coord.row < self.height and
			coord.col >= 0 and 
			coord.col < self.width 
		)


	def valid_neighbors(self, coord):
		for neighbor in coord.neighbors:
			if self.is_valid(neighbor):
				yield neighbor

	def value(self, coord):
		if not self.is_valid(coord):
			return None
		return self.heightmap[coord]

	def risk(self, coord):
		if not self.is_valid(coord):
			return None
		return self.heightmap[coord] + 1

	def is_low_point(self, coord):
		if not self.is_valid(coord):
			return False
		value = self.heightmap[coord]
		for neighbor in coord.neighbors:
			if not self.is_valid(neighbor):
				continue
			if self.heightmap[neighbor] <= value:
				return False

		return True



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
	def neighbors(self):
		yield Coord(self.row+1, self.col)
		yield Coord(self.row-1, self.col)
		yield Coord(self.row, self.col+1)
		yield Coord(self.row, self.col-1)


cavemap = CaveMap()
row = 0
for line in file.readlines():
	col = 0
	for val in line.strip():
		cavemap.add_coord(Coord(row, col), int(val))
		col += 1
	row += 1
cavemap.initialize_low_points()
cavemap.initialize_basins()

sizes = []
for basin in cavemap.basins:
	sizes.append(len(basin))

count = 3
result = 1
for size in reversed(sorted(sizes)):
	result *= size
	count -= 1
	if count <= 0:
		break

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)















