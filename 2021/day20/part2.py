from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

class Map2D:
	def __init__(self, defaultval = False):
		self.map = {}
		self.colmin = 0
		self.rowmin = 0
		self.colmax = 0
		self.rowmax = 0
		self.defaultval = defaultval


	def __str__(self):
		return str(self.map)


	def __repr__(self):
		return str(self.map)


	def __getitem__(self, coord):
		if not self.is_valid(coord):
			return self.defaultval
		return self.map[coord] if coord in self.map else False


	def __setitem__(self, coord, value):
		self.add_coord(coord, value)


	@property
	def coords(self):
		for i in range(self.rowmin, self.rowmax):
			for j in range(self.colmin, self.colmax):
				yield Coord(i,j)


	@property
	def coords_with_border(self):
		for i in range(self.rowmin - 1, self.rowmax + 1):
			for j in range(self.colmin - 1, self.colmax + 1):
				yield Coord(i,j)


	def add_coord(self, coord, value):
		self.map[coord] = value
		if coord.row >= self.rowmax:
			self.rowmax = coord.row + 1
		if coord.row < self.rowmin:
			self.rowmin = coord.row
		if coord.col >= self.colmax:
			self.colmax = coord.col + 1
		if coord.col < self.colmin:
			self.colmin = coord.col


	def is_valid_with_border(self, coord):
		return (
			coord.row >= self.rowmin - 1 and 
			coord.row < self.rowmax + 1 and
			coord.col >= self.colmin - 1 and 
			coord.col < self.colmax + 1)


	def is_valid(self, coord):
		return (
			coord.row >= self.rowmin and 
			coord.row < self.rowmax and
			coord.col >= self.colmin and 
			coord.col < self.colmax)


	def valid_neighbors(self, coord): #prolly don't need?
		for neighbor in coord.neighbors:
			if self.is_valid(neighbor):
				yield neighbor

	def debug(self):
		for i in range(self.rowmin, self.rowmax):
			s = ""
			for j in range(self.colmin, self.colmax):
				s += str(self[Coord(i,j)])
			print s
		print ""

	def count(self, target):
		total = 0
		if self.defaultval == "#":
			float("inf")
		for coord in self.coords:
			if self[coord] == target:
				total += 1
		return total



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
			self.col == other.col)

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

	@property
	def square(self):
		yield Coord(self.row-1, self.col-1)
		yield Coord(self.row-1, self.col)
		yield Coord(self.row-1, self.col+1) 
		yield Coord(self.row, self.col-1)
		yield self
		yield Coord(self.row, self.col+1)
		yield Coord(self.row+1, self.col-1)
		yield Coord(self.row+1, self.col)
		yield Coord(self.row+1, self.col+1)


def parse_bit(bit):
	return 0 if bit == "." else 1


def convert_bit(binarynum, enhancement):
	return enhancement[binarynum]


def next_default(image, enhancement):
	if image.defaultval == ".":
		return enhancement[0]
	else:
		return enhancement[-1]


def apply_enhancement(image, enhancement, coord):
	binarynum = 0
	# debug = ""
	for neighbor in coord.square:
		bit = image[neighbor]
		# debug += bit
		binarynum <<= 1
		binarynum |= parse_bit(bit)
	# print debug, binarynum
	return convert_bit(binarynum, enhancement)


def enhance(image, enhancement):
	newimage = Map2D(next_default(image, enhancement))
	for coord in image.coords_with_border:
		newimage.add_coord(coord, apply_enhancement(image, enhancement, coord))
	return newimage


lines = file.readlines()
enhancement = lines[0].strip()
image = Map2D(".")
row = 0
for line in lines[2:]:
	col = 0
	for val in line.strip():
		image.add_coord(Coord(row, col), val)
		col += 1
	row += 1

# image.debug()

steps = 50
for step in range(0, steps):
	print step
	image = enhance(image, enhancement)
	# image.debug()

result = image.count("#")
print("Completed in %fms" % ((timer() - start) * 1000))
image.debug()
print("%d is the result" % result)











