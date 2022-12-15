from timeit import default_timer as timer
import re

start = timer()

def manhattan(a, b):
	return abs(a[1] - b[1]) + abs(a[0] - b[0])

def iter_x_range(origin, dist, fixedy):
	dist -= abs(fixedy - origin[1]) # y takes up distance
	return range(origin[0] - dist, origin[0] + dist)

class Sensor:
	def __init__(self, pos, closest):
		self.pos = pos
		self.closest = closest
		self.range = manhattan(pos, closest)

	def is_within_range(self, y):
		return abs(self.pos[1] - y) < self.range

	def __str__(self):
		return "[%s:%d]" % (str(self.pos), self.range)

	def __repr__(self):
		return str(self)


class Beacon:
	def __init__(self, pos):
		self.pos = pos
		self.sensors = []


class Empty:
	def __init__(self, pos):
		self.pos = pos
		self.sensors = []


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

	def debug(self):
		s = ""
		for x in range(self.min[0], self.max[0] + 1):
			if x % 5 == 0:
				s += str(x/5)
			else:
				s += " "
		print s

		for y in range(self.min[1], self.max[1] + 1):
			s = ""
			for x in range(self.min[0], self.max[0] + 1):
				val = self[(x,y)]
				if val is None:
					s += "."
				elif isinstance(val, Beacon):
					s += "B"
				elif isinstance(val, Sensor):
					s += "S"
				elif isinstance(val, Empty):
					s += "#"

			print s

cavemap = DefaultValueMap(None)
sensors = []
beacons = []

with open('input.txt') as file:
	pattern = re.compile(r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)")
	for match in pattern.finditer(file.read()):
		sensor_pos = tuple(int(num) for num in match.group(1,2))
		beacon_pos = tuple(int(num) for num in match.group(3,4))

		sensor = Sensor(sensor_pos, beacon_pos)
		cavemap[sensor_pos] = sensor
		sensors.append(sensor)

		beacon = cavemap[beacon_pos]
		if beacon is None:
			beacon = Beacon(beacon_pos)
			cavemap[beacon_pos] = beacon
			beacons.append(beacon)
		beacon.sensors.append(sensor_pos)

y = 2000000

positions = set()
for sensor in sensors:
	if sensor.is_within_range(y):
		positions.update(iter_x_range(sensor.pos, sensor.range, y))

result = len(positions)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)