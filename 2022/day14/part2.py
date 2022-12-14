from timeit import default_timer as timer

start = timer()

fall_origin = (500,0)

empty = "."
sand_hole = "+"
resting_sand = "o"
rock = "#"


class DefaultValueMap:
	def __init__(self, default = None):
		self.map = {}
		self.default = default
		self.min = None
		self.max = None

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
		self.update_limits(key)

	def update_limits(self, key):
		if self.min is None:
			self.min = [key[0], key[1]]
		else:
			if key[0] < self.min[0]:
				self.min[0] = key[0]
			if key[1] < self.min[1]:
				self.min[1] = key[1]

		if self.max is None:
			self.max = [key[0], key[1]]
		else:
			if key[0] > self.max[0]:
				self.max[0] = key[0]
			if key[1] > self.max[1]:
				self.max[1] = key[1]

	def pop(self, key):
		return self.map.pop(key)


def values(a, b, pos):
	if a[pos] <= b[pos]:
		return range(int(a[pos]), int(b[pos]) + 1)
	return range(int(b[pos]), int(a[pos]) + 1)


def fill_segment(cavemap, a, b):
	for x in values(a, b, 0):
		for y in values(a, b, 1):
			cavemap[(x,y)] = rock

def debug_map(cavemap):
	for y in range(cavemap.min[1], cavemap.max[1] + 1):
		s = ""
		for x in range(cavemap.min[0], cavemap.max[0] + 1):
			point = (x,y)
			s += cavemap[(x,y)]
		print s


def get_next_loc(cavemap, loc):
	(x,y) = loc
	loc = (x, y + 1)
	if cavemap[loc] == empty:
		return loc
	loc = (x - 1, y + 1)
	if cavemap[loc] == empty:
		return loc
	loc = (x + 1, y + 1)
	if cavemap[loc] == empty:
		return loc
	return None



def drop_sand(cavemap): # drop until rest - None if infinite
	loc = fall_origin
	while True:
		next_loc = get_next_loc(cavemap, loc)
		if next_loc is None:
			return loc
		if next_loc[1] >= cavemap.max[1]: # hit the bottom
			return loc
		loc = next_loc


cavemap = DefaultValueMap(empty)
cavemap[fall_origin] = sand_hole
with open('input.txt') as file:
	for line in file.readlines():
		points = [i.split(",") for i in line.strip().split(" -> ")]
		for i in range(len(points) - 1):
			# print "segment", points[i], points[i+1]
			fill_segment(cavemap, points[i], points[i+1])
cavemap.max[1] += 2 # hacky but whatever
# debug_map(cavemap)

result = 0
while True:
	loc = drop_sand(cavemap)
	cavemap[loc] = resting_sand
	result += 1	
	if loc == fall_origin:
		break

# debug_map(cavemap)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)