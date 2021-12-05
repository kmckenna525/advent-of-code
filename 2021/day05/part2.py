from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

class VentLine:
	def __init__(self, start, end):
		self.x1 = start[0]
		self.x2 = end[0]
		self.y1 = start[1]
		self.y2 = end[1]

	@property
	def start(self):
		return (self.x1, self.y1)

	@property
	def end(self):
		return (self.x2, self.y2)

	@property
	def xmin(self):
		return min(self.x1, self.x2)

	@property
	def xmax(self):
		return max(self.x1, self.x2)

	@property
	def ymin(self):
		return min(self.y1, self.y2)

	@property
	def ymax(self):
		return max(self.y1, self.y2)

	@property
	def slope(self):
		xdiff = (self.x2 - self.x1)
		if xdiff == 0:
			return None
		return float(self.y2 - self.y1) / float(self.x2 - self.x1)

	@property
	def is_straight(self):
		return self.x1 == self.x2 or self.y1 == self.y2

	@property
	def points(self):
		slope = self.slope
		if slope is None:
			for y in range(self.ymin, self.ymax + 1): #inclusive
				yield (self.x1, y)
		elif slope == 0:
			for x in range(self.xmin, self.xmax + 1): #inclusive
				yield (x, self.y1)
		else:
			x1 = self.x1
			y1 = self.y1
			for x in range(self.xmin, self.xmax + 1): #inclusive
				yield (x, y1 + int((x - x1) * slope))


	def intersections(self, other):
		other_points = set(other.points)
		for point in self.points:
			if point in other_points:
				yield point

	def __str__(self):
		return  "%s, %s" % (str(self.start), str(self.end))

	def __repr__(self):
		return  "%s, %s" % (str(self.start), str(self.end))

ventlines = []

pattern = r"(?P<x1>.+),(?P<y1>.+) -> (?P<x2>.+),(?P<y2>.+)";
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	x1 = int(data["x1"])
	y1 = int(data["y1"])
	x2 = int(data["x2"])
	y2 = int(data["y2"])


	ventline = VentLine((x1,y1),(x2,y2))
	ventlines.append(ventline)

length = len(ventlines)

# get possible intersections
all_intersections = set()
for i in range(0, length):
	for j in range(i + 1, length):
		first = ventlines[i]
		second = ventlines[j]
		for coord in first.intersections(second):
			all_intersections.add(coord)

result = len(all_intersections)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)