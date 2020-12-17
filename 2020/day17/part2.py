from timeit import default_timer as timer
from collections import namedtuple

iterations = 6

Point = namedtuple("Point", "x y z w")
Point.__new__.__defaults__ = (0,0,0,0)

def neighbors(root):
	for dirx in range(-1,2):
		for diry in range(-1,2):
			for dirz in range(-1,2):
				for dirw in range(-1,2):
					if dirx == 0 and diry == 0 and dirz == 0 and dirw == 0:
						continue
					x = dirx + root.x
					y = diry + root.y
					z = dirz + root.z
					w = dirw + root.w
					# print (x,y,z)
					yield Point(x,y,z,w)

class Grid:
	def __init__(self):
		self.grid = {}
		self.copy = {}
		self.dimx = (0,0)
		self.dimy = (0,0)
		self.dimz = (0,0)
		self.dimw = (0,0)

	def __str__(self):
		return  "%d x %d x %d x %d" % (self.width, self.height, self.depth, self.wobble)

	def __repr__(self):
		return  "%d x %d x %d x %d" % (self.width, self.height, self.depth, self.wobble)

	@property
	def width(self):
		return self.dimx[1] - self.dimx[0]

	@property
	def height(self):
		return self.dimy[1] - self.dimy[0]

	@property
	def depth(self):
		return self.dimz[1] - self.dimz[0]

	@property
	def wobble(self):
		return self.dimw[1] - self.dimw[0]
	

	def get(self, point):
		if point in self.grid:
			return self.grid[point]
		return 0

	def prep(self, point, val):
		if val > 0:
			self.copy[point] = val
		elif point in self.copy:
			del self.copy[point]

	def commit(self):
		self.grid = {}
		self.grid.update(self.copy)
		self.update_limits()

	def update_limits(self):
		X = None
		Y = None
		Z = None
		W = None
		x = None
		y = None
		z = None
		w = None
		for point in self.grid.keys():
			# print point
			if x is None or point.x < x:
				x = point.x
			if X is None or point.x > X:
				X = point.x
			if y is None or point.y < y:
				y = point.y
			if Y is None or point.y > Y:
				Y = point.y
			if z is None or point.z < z:
				z = point.z
			if Z is None or point.z > Z:
				Z = point.z
			if w is None or point.w < w:
				w = point.w
			if W is None or point.w > W:
				W = point.w
			# print (x,y,z)
			# print (X,Y,Z)
		self.dimx = (x,X)
		self.dimy = (y,Y)
		self.dimz = (z,Z)
		self.dimw = (w,W)

	def keys(self, buffer = 0):
		minx = self.dimx[0]
		maxx = self.dimx[1]
		miny = self.dimy[0]
		maxy = self.dimy[1]
		minz = self.dimz[0]
		maxz = self.dimz[1]
		minw = self.dimw[0]
		maxw = self.dimw[1]
		for x in range(minx - buffer, maxx + 1 + buffer):
			for y in range(miny - buffer, maxy + 1 + buffer):
				for z in range(minz - buffer, maxz + 1 + buffer):
					for w in range(minw - buffer, maxw + 1 + buffer):
						yield Point(x,y,z,w)

	def values(self, buffer = 0):
		for point in self.keys(buffer):
			yield self.get(point)

	def items(self, buffer = 0):
		for point in self.keys(buffer):
			yield (point, self.get(point))

	def log(self):
		for w in range(self.dimw[0], self.dimw[1] + 1):
			for z in range(self.dimz[0], self.dimz[1] + 1):
				print("z=%d, w=%d, x(%d,%d), y(%d,%d)"%(z,w,self.dimx[0], self.dimx[1],self.dimy[0], self.dimy[1]))
				for y in range(self.dimy[0], self.dimy[1] + 1):
					row = ""
					for x in range(self.dimx[0], self.dimx[1] + 1):
						val = self.get(Point(x,y,z,w))
						if val == 0:
							row += "."
						if val == 1:
							row += "#"
					print(row)
				print



start = timer()
file = open('input.txt')

# process input, 0 off # on
grid = Grid()
y = 0
for line in file.readlines():
	x = 0
	for char in line.strip():
		if char == "#":
			grid.prep(Point(x, y), 1)
		if char == ".":
			grid.prep(Point(x, y), 0)
		x += 1
	y += 1

grid.commit()


def should_turn_off(point, target_min, target_max):
	total = 0
	for neighbor in neighbors(point):
		if grid.get(neighbor) == 1:
			total += 1
			if total > target_max:
				return True
	return total < target_min or total > target_max

def should_turn_on(point, target):
	total = 0
	for neighbor in neighbors(point):
		if grid.get(neighbor) == 1:
			total += 1
			if total > target:
				return False
	return total == target

# grid.log()

# start the rules
for i in range(0, iterations):
	# run rules
	for (point, val) in grid.items(1):
		# check off
		if val == 0 and should_turn_on(point, 3):
			grid.prep(point, 1)
			continue

		# check on
		if val == 1 and should_turn_off(point, 2, 3):
			grid.prep(point, 0)
			continue

	grid.commit()
	# print("After %d cycle:" % (i + 1))
	# grid.log()

# count active
result = 0
for val in grid.values():
	if val == 1:
		result += 1


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)