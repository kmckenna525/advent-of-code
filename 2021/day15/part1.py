from timeit import default_timer as timer
import re
from queue import PriorityQueue

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
		yield Coord(self.row+1, self.col)
		yield Coord(self.row-1, self.col)
		yield Coord(self.row, self.col+1)
		yield Coord(self.row, self.col-1)

		
riskmap = Map2D()
row = 0
for line in file.readlines():
	col = 0
	for val in line.strip():
		riskmap.add_coord(Coord(row, col), int(val))
		col += 1
	row += 1

result = 0

seen = {} # coord: (distance, path)
unseen = PriorityQueue() # (distance, path, coord)
unseen.put((0, [Coord(0,0)])) 
target = Coord(riskmap.height - 1, riskmap.width - 1)
result = float("inf")
while not unseen.empty():
	dist, path = unseen.get()
	coord = path[-1]
	if coord == target and dist < result:
		result = dist
		break

	if coord in seen and seen[coord][0] <= dist:
		# coord has already existed at a lower or equal cost
		continue

	seen[coord] = (dist, path)

	for neighbor in riskmap.valid_neighbors(coord):
		nextlist = list(path)
		nextlist.append(neighbor)
		unseen.put((dist + riskmap[neighbor], nextlist))

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)