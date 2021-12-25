from timeit import default_timer as timer
from collections import namedtuple

Coord = namedtuple('Coord', ['row','col'])

class WraparoundMap2D:
	def __init__(self):
		self.map = {}
		self.width = 0
		self.height = 0


	def __str__(self):
		return str(self.map)


	def __repr__(self):
		return str(self.map)


	def __getitem__(self, coord):
		coord = Coord(coord.row % self.height, coord.col % self.width)
		return self.map[coord]


	def __setitem__(self, coord, value):
		coord = Coord(coord.row % self.height, coord.col % self.width)
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

	def debug(self):
		for i in range(0, self.height):
			s = ""
			for j in range(0, self.width):
				s += str(self[Coord(i,j)])
			print s
		print ""


def get_next(cucumber_map, coord, cucumber):
	if cucumber == ">":
		return Coord(coord.row, coord.col + 1)
	if cucumber == "v":
		return Coord(coord.row + 1, coord.col)



def will_move(cucumber_map, coord, herd):
	cucumber = cucumber_map[coord]
	if cucumber != herd:
		return False
	# print coord, get_next(cucumber_map, coord, cucumber), cucumber
	return cucumber_map[get_next(cucumber_map, coord, cucumber)] == "."


def movable_cucumbers(cucumber_map, herd):
	movable = []
	for coord in cucumber_map.coords:
		if will_move(cucumber_map, coord, herd):
			# print "move", coord
			movable.append(coord)
	return movable


def move(cucumber_map, coord):
	cucumber = cucumber_map[coord]
	cucumber_map[coord] = "."
	cucumber_map[get_next(cucumber_map, coord, cucumber)] = cucumber


def step(cucumber_map):
	didmove = False
	for coord in movable_cucumbers(cucumber_map, ">"):
		didmove = True
		move(cucumber_map, coord)
	for coord in movable_cucumbers(cucumber_map, "v"):
		didmove = True
		move(cucumber_map, coord)
	return didmove


start = timer()
file = open('input.txt')

cucumber_map = WraparoundMap2D()
row = 0
for line in file.readlines():
	col = 0
	for val in line.strip():
		cucumber_map.add_coord(Coord(row, col), val)
		col += 1
	row += 1
# cucumber_map.debug()

result = 1
while step(cucumber_map):
	# cucumber_map.debug()
	result += 1
	if result %100 == 0:
		print result
# for i in range(0, 5):
# 	step(cucumber_map)
# 	cucumber_map.debug()


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)