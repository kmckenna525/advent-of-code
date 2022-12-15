from timeit import default_timer as timer
import re

start = timer()

def manhattan(a, b):
	return abs(a[1] - b[1]) + abs(a[0] - b[0])

def get_ranges(sensors, fixedy): 
	# do it like the cubes from previous year by condensing intersecting ranges
	ranges = []
	for sensor in sensors:
		if not sensor.is_within_range(fixedy):
			continue
		ranges.append(x_range(sensor.pos, sensor.range, fixedy))

	ranges.sort() # sorts by the range[0] value
	i = 1
	# print ranges
	while(i < len(ranges)):
		a = ranges[i - 1]
		b = ranges[i]
		if a[1] + 1 >= b[0]:
			a[1] = max(b[1], a[1]) # a already has the correct min at [0] from the sort
			ranges.pop(i)
			continue # don't increment, we'll try a on the next element first
		i += 1
	# print ranges
	return ranges

def x_range(origin, dist, fixedy):
	dist -= abs(fixedy - origin[1]) # y takes up distance
	return [origin[0] - dist, origin[0] + dist] # array so its writeable

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


sensors = []
with open('input.txt') as file:
	pattern = re.compile(r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)")
	for match in pattern.finditer(file.read()):
		sensor_pos = tuple(int(num) for num in match.group(1,2))
		beacon_pos = tuple(int(num) for num in match.group(3,4))

		sensor = Sensor(sensor_pos, beacon_pos)
		sensors.append(sensor)

def get_distress(maxval):
	for y in range(0, maxval + 1):
		# print y
		ranges = get_ranges(sensors, y)
		if len(ranges) > 1:
			x = ranges[0][1] + 1
			# print(x,y)
			return x * 4000000 + y
				

# result = get_distress(20)
result = get_distress(4000000)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)