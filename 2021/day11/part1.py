from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

class Map2D:
	def __init__(self):
		self.map = {}
		self.width = 0
		self.height = 0


	def __str__(self):
		return str(self.map)


	def __repr__(self):
		return str(self.map)


	def __getitem__(self, coord):
		return self.map[coord]


	def __setitem__(self, coord, value):
		self.map[coord] = value


	@property
	def coords(self):
		for i in range(0, self.height):
			for j in range(0, self.width):
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
			coord.row < self.height and
			coord.col >= 0 and 
			coord.col < self.width 
		)


	def valid_neighbors(self, coord):
		for neighbor in coord.neighbors:
			if self.is_valid(neighbor):
				yield neighbor

	def debug(self):
		for i in range(0, self.height):
			s = ""
			for j in range(0, self.width):
				s += str(self[Coord(i,j)])
			print s
		print ""





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
		yield Coord(self.row-1, self.col-1)
		yield Coord(self.row-1, self.col)
		yield Coord(self.row-1, self.col+1)
		yield Coord(self.row, self.col-1)
		yield Coord(self.row, self.col+1)
		yield Coord(self.row+1, self.col-1)
		yield Coord(self.row+1, self.col)
		yield Coord(self.row+1, self.col+1)


def try_flash(octopi, coord, flashed):
	if coord not in flashed and octopi[coord] > 9:
		flashed.add(coord)
		for neighbor in octopi.valid_neighbors(coord):
			octopi[neighbor] += 1
			try_flash(octopi, neighbor, flashed)

def step(octopi):
	for coord in octopi.coords:
		octopi[coord] += 1

	flashed = set()
	for coord in octopi.coords:
		try_flash(octopi, coord, flashed)

	for coord in flashed:
		octopi[coord] = 0

	return len(flashed)

		
octopi = Map2D()
row = 0
for line in file.readlines():
	col = 0
	for val in line.strip():
		octopi.add_coord(Coord(row, col), int(val))
		col += 1
	row += 1

result = 0
steps = 100
# octopi.debug()
for i in range(0,steps):
	result += step(octopi)
	# octopi.debug()

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)