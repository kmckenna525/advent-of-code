from timeit import default_timer as timer
from collections import namedtuple
import re

start = timer()
file = open('input.txt')

Instruction = namedtuple('Instruction', ['on', 'cuboid'])
Coord = namedtuple('Coord', ['x','y','z'])
Range = namedtuple('Range', ['min','max'])

def make_cuboid(xmin, xmax, ymin, ymax, zmin, zmax):
	return Coord(Range(xmin, xmax), Range(ymin, ymax), Range(zmin, zmax))

def does_intersect(a, b):
	if a.x.min > b.x.max or a.x.max < b.x.min:
		return False
	if a.y.min > b.y.max or a.y.max < b.y.min:
		return False
	if a.z.min > b.z.max or a.z.max < b.z.min:
		return False
	return True

def intersect_possibilities(a, b):
	possibilities = []

	# just slice them cubes up into littler cubes at the intersections
	if a.x.min > b.x.min:
		possibilities.append(make_cuboid(b.x.min, a.x.min - 1, b.y.min, b.y.max, b.z.min, b.z.max))
	if a.x.max < b.x.max:
		possibilities.append(make_cuboid(a.x.max + 1, b.x.max, b.y.min, b.y.max, b.z.min, b.z.max))
	if a.y.min > b.y.min:
		possibilities.append(make_cuboid(max(b.x.min, a.x.min), min(b.x.max, a.x.max), b.y.min, a.y.min - 1, b.z.min, b.z.max))
	if a.y.max < b.y.max:
		possibilities.append(make_cuboid(max(b.x.min, a.x.min), min(b.x.max, a.x.max), a.y.max + 1, b.y.max, b.z.min, b.z.max))
	if a.z.min > b.z.min:
		possibilities.append(make_cuboid(max(b.x.min, a.x.min), min(b.x.max, a.x.max), max(b.y.min, a.y.min), min(b.y.max, a.y.max), b.z.min, a.z.min - 1))
	if a.z.max < b.z.max:
		possibilities.append(make_cuboid(max(b.x.min, a.x.min), min(b.x.max, a.x.max), max(b.y.min, a.y.min), min(b.y.max, a.y.max), a.z.max + 1, b.z.max))

	return possibilities


def volume(cuboid):
	return (
		(cuboid.x.max - cuboid.x.min + 1) * 
		(cuboid.y.max - cuboid.y.min + 1) * 
		(cuboid.z.max - cuboid.z.min + 1))


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

	ranges.append(Instruction(on, make_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)))


oncubes = []
for instr in ranges:
	for i in range(len(oncubes)):
		cuboid = oncubes[i]
		if not does_intersect(instr.cuboid, cuboid):
			continue
		oncubes[i] = None
		possibilities = intersect_possibilities(instr.cuboid, cuboid)
		oncubes += possibilities

	if instr.on:
		oncubes.append(instr.cuboid)
		# (xmin, xmax), (ymin, ymax), (zmin, zmax) = instr.cuboid
		# oncubes.append(make_cuboid(min(xmin, xmax), max(xmin, xmax), min(ymin, ymax), max(ymin, ymax), min(zmin, zmax), max(zmin, zmax)))

	for i in list(reversed(range(len(oncubes)))):
		if oncubes[i] is None:
			oncubes.pop(i)

result = 0
for cuboid in oncubes:
	result += volume(cuboid)


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)