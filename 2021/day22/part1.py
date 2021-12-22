from timeit import default_timer as timer
from collections import namedtuple
import re

start = timer()
file = open('input.txt')

Instruction = namedtuple('Instruction', ['on', 'cuboid'])
Coord = namedtuple('Coord', ['x','y','z'])
Range = namedtuple('Range', ['min','max'])

class Map2D:
	def __init__(self, defaultval = False):
		self.map = {}
		self.xrange = Range(0,0) 
		self.yrange = Range(0,0) 
		self.zrange = Range(0,0) 
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
		for i in range(self.xrange.min, self.xrange.max):
			for j in range(self.yrange.min, self.yrange.max):
				for k in range(self.zrange.min, self.zrange.max):
					yield Coord(i,j,k)


	def add_coord(self, coord, value):
		self.map[coord] = value
		if coord.x >= self.xrange.max:
			self.xrange = Range(self.xrange.min, coord.x + 1)
		if coord.x < self.xrange.min:
			self.xrange = Range(coord.x, self.xrange.max)
		if coord.y >= self.yrange.max:
			self.yrange = Range(self.yrange.min,  coord.y + 1)
		if coord.y < self.yrange.min:
			self.yrange = Range(coord.y, self.yrange.max)
		if coord.z >= self.zrange.max:
			self.zrange = Range(self.zrange.min,  coord.z + 1)
		if coord.z < self.zrange.min:
			self.zrange = Range(coord.z, self.zrange.max)


	def is_valid(self, coord):
		return (
			coord.x >= self.xrange.min and 
			coord.x < self.xrange.max and
			coord.y >= self.yrange.min and 
			coord.y < self.yrange.max and
			coord.z >= self.zrange.min and 
			coord.z < self.zrange.max)


	def valid_neighbors(self, coord): 
		for neighbor in coord.neighbors:
			if self.is_valid(neighbor):
				yield neighbor


	def debug(self):
		for i in range(self.xrange.min, self.xrange.max):
			s = ""
			for j in range(self.yrange.min, self.yrange.max):
				s += str(self[Coord(i,j)])
			print s
		print ""


	def count(self, target):
		total = 0
		for coord in self.coords:
			if self[coord] == target:
				total += 1
		return total


def is_within_range(coordrange):
	return (
		coordrange.min >= -500 and
		coordrange.max <= 500)


def is_within_region(instruction):
	return (
		is_within_range(instruction.cuboid.x) and
		is_within_range(instruction.cuboid.y) and
		is_within_range(instruction.cuboid.z))


def execute(instruction, fullmap):
	for x in range(instruction.cuboid.x.min, instruction.cuboid.x.max + 1): 
		for y in range(instruction.cuboid.y.min, instruction.cuboid.y.max + 1): 
			for z in range(instruction.cuboid.z.min, instruction.cuboid.z.max + 1): 
				coord = Coord(x,y,z)
				fullmap[coord] = instruction.on


pattern = r"(?P<on>on|off) x=(?P<xmin>.+)\.\.(?P<xmax>.+),y=(?P<ymin>.+)\.\.(?P<ymax>.+),z=(?P<zmin>.+)\.\.(?P<zmax>.+)"
ranges = []
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict()
	on = data["on"] == "on"
	xmin = int(data["xmin"])
	xmax = int(data["xmax"])
	ymin = int(data["ymin"])
	ymax = int(data["ymax"])
	zmin = int(data["zmin"])
	zmax = int(data["zmax"])

	ranges.append(Instruction(on, Coord(Range(xmin, xmax), Range(ymin, ymax), Range(zmin, zmax))))


fullmap = Map2D()
for instr in ranges:
	if is_within_region(instr):
		execute(instr, fullmap)


result = fullmap.count(True)


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)