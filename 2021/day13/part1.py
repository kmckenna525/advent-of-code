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
		if not self.is_valid(coord):
			return False
		return self.map[coord] if coord in self.map else False


	def __setitem__(self, coord, value):
		self.add_coord(coord, value)


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


	@property
	def count(self):
		total = 0
		for coord in self.coords:
			if self[coord]:
				total += 1
		return total

	def foldx(self, value):
		for col in range(value, self.width):
			for row in range(0, self.height):
				coord = Coord(row, col)
				if coord in self.map and self[coord]:
					self.add_coord(Coord(row, (value - (col - value))), True)
		self.width = value

	def foldy(self, value):
		for row in range(value, self.height):
			for col in range(0, self.width):
				coord = Coord(row, col)
				if coord in self.map and self[coord]:
					self.add_coord(Coord((value - (row - value)), col), True)
		self.height = value


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

pattern_coord = r"(?P<x>\d+),(?P<y>\d+)";
pattern_fold = r"fold along (x=(?P<x>\d+)|y=(?P<y>\d+))";
coords = True
paper = Map2D()
result = 0
for line in file.readlines():
	if coords:
		if line.strip() == "":
			coords = False
			continue
		matches = re.match(pattern_coord, line)
		data = matches.groupdict();
		x = int(data["x"])
		y = int(data["y"])
		paper.add_coord(Coord(y, x), True)
	else:
		matches = re.match(pattern_fold, line)
		data = matches.groupdict();
		x = data["x"]
		y = data["y"]

		if x: 
			paper.foldx(int(x))
			result = paper.count
			break
		elif y:
			paper.foldy(int(y))
			result = paper.count
			break


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)