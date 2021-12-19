from timeit import default_timer as timer
import re
import json
from itertools import combinations
import math

start = timer()
file = open('input.txt')

class Vector:
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
		self.as_set = set([abs(x),abs(y),abs(z)])
		self.as_map = {abs(x):0, abs(y):1, abs(z):2}

	def __str__(self):
		return  "(%d,%d,%d)" % (self.x, self.y, self.z)

	def __repr__(self):
		return  "(%d,%d,%d)" % (self.x, self.y, self.z)

	def __hash__(self):
		 return hash((self.x, self.y, self.z))

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.x == other.x and
			self.y == other.y and 
			self.z == other.z)

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, other):
		return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

	def __getitem__(self, key):
		if key == 0:
			return self.x
		if key == 1:
			return self.y
		if key == 2:
			return self.z

	@property
	def magnitude(self):
		return math.sqrt(
			math.pow(self.x, 2) +
			math.pow(self.y, 2) +
			math.pow(self.z, 2))
	

	def similar(self, other):
		return self.as_set == other.as_set

	def manhattan(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

	def get_inverse(self, val):
		axis = self.as_map[abs(val)]
		return (
			axis, 
			get_flipper(self[axis], val))

	def apply_map(self, instructions):
		out = self
		for op in instructions:
			if type(op) is tuple:
				out = out.apply_rotation(op)
			elif isinstance(op, Vector):
				out = out.apply_translation(op)
			else:
				print "UNRECOGNIZED OPERATION", op, type(op), op is Vector
		return out

	def apply_rotation(self, rotmap):
		return Vector(
			self[rotmap[0][0]] * rotmap[0][1],
			self[rotmap[1][0]] * rotmap[1][1],
			self[rotmap[2][0]] * rotmap[2][1],
			)

	def apply_translation(self, offset):
		return self + offset

	def get_mapping_func(self, other):
		if len(self.as_map) == 0:
			return None

		return (
			other.get_inverse(self.x), 
			other.get_inverse(self.y), 
			other.get_inverse(self.z))


class Region:
	def __init__(self):
		self.scanners = []
		self.basis = None
		self.known = set()
		self.beacons = {} # positions relative to the first scanner to [scanners]
		self.rotmaps = {} # (scannera, scannerb) => (btoa, atob)
		self.overlaps = {} # scanner => {other => (btoa, atob)}


	def __str__(self):
		s = ""
		for scanner in self.scanners:
			s += str(scanner) + "\n"
		return s


	def __repr__(self):
		return  str(self)


	def addscanner(self, scanner):
		self.scanners.append(scanner)
		scanner.initneighbors()
		self.overlaps[scanner] = {}
		if self.basis is None:
			self.basis = scanner
			for beacon in scanner.detected:
				self.beacons[beacon.position] = set([scanner])

	def get_highest_distance(self):
		highest = 0
		for a,b in combinations(self.scanners, 2):
			dist = a.position.manhattan(b.position)
			if dist > highest:
				print a, b, dist
				highest = dist

		return highest


	def initmap(self):
		self.basis = self.scanners[0]
		for a,b in combinations(self.scanners, 2):
			# print a.id, "vs", b.id
			rotmaps = a.overlaps(b, target)
			if rotmaps is not None:
				print "OVERLAP", a.id, b.id
				btoa, atob = rotmaps
				self.spread_overlaps(a, b, atob, btoa)
				self.overlaps[a][b] = (atob, btoa)
				self.overlaps[b][a] = (btoa, atob)
				# for beacon in a.detected:
				# 	print "  OLD", beacon.position
				# for beacon in b.detected:
				# 	print "  NEW", beacon.position.apply_map(btoa) 
		for scanner in self.scanners[1:]: # all but basis
			scanner.position
			if self.basis not in self.overlaps[scanner]:
				print scanner.id, self.overlaps[scanner].keys()
				found = False
				for other, (stoo, otos) in self.overlaps[scanner].items():
					print "  CHECK", other.id, self.overlaps[other].keys()
					if other in self.overlaps[self.basis]:
						btoo, otob = self.overlaps[self.basis][other]
						self.spread_overlaps_specific(other, self.basis, otob, btoo, scanner, otos, stoo)
						found = True
				if not found:
					print "FOUND NOTHING"
			self.add_points(scanner)
		for scanner in self.scanners[1:]:
			scanner.position = Vector().apply_map(self.overlaps[scanner][self.basis][0])
			print scanner, scanner.position





	def spread_overlaps_specific(self, a, b, atob, btoa, other, atoother, othertoa):
		othertob = ctoa(othertoa, atob)
		btoother = ctoa(btoa, atoother)
		self.overlaps[other][b] = (othertob, btoother)
		self.overlaps[b][other] = (btoother, othertob)



	def spread_overlaps(self, a, b, atob, btoa):
		for other, (atoother, othertoa) in self.overlaps[a].items():
			if b == other:
				continue
			# only if basis is not yet in there and b not already in there, if basis there we are good
			if b not in self.overlaps[other] and self.basis not in self.overlaps[other]:
				othertob = ctoa(othertoa, atob)
				btoother = ctoa(btoa, atoother)
				self.overlaps[other][b] = (othertob, btoother)
				self.overlaps[b][other] = (btoother, othertob)
				self.spread_overlaps(other, b, othertob, btoother)
		for other, (btoother, othertob) in self.overlaps[b].items():
			if a == other:
				continue
			# only if basis is not yet in there and a not already in there, if basis there we are good
			if a not in self.overlaps[other] and self.basis not in self.overlaps[other]:
				# print "  ANOTHER", other.id, othertob, btoa
				othertoa = ctoa(othertob, btoa)
				# testctoa(othertob, btoa, other.detected[0].position)
				atoother = ctoa(atob, btoother)
				# testctoa(atob, btoother, a.detected[0].position)
				self.overlaps[other][a] = (othertoa, atoother)
				self.overlaps[a][other] = (atoother, othertoa)
				self.spread_overlaps(other, a, othertoa, atoother)
				# for beacon in other.detected:
				# 	print "    NEWERER", beacon.position.apply_map(othertoa) 


	def add_points(self, scanner):
		for beacon in scanner.detected:
			stob, btos = self.overlaps[scanner][self.basis]
			newpos = beacon.position.apply_map(stob)
			if newpos in self.beacons:
				self.beacons[newpos].add(scanner)
			else:
				self.beacons[newpos] = set([scanner])



class Scanner:
	def __init__(self, id):
		self.id = id
		self.detected = []
		self.position = Vector()

	def __str__(self):
		return  "%d" % (self.id)

	def __repr__(self):
		return str(self)
		# return  "%d: %s" % (self.id, str(self.detected))

	def add(self, beacon):
		self.detected.append(beacon)

	def __hash__(self):
		 return hash(self.id)

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.id == other.id)

	def initneighbors(self):
		for i in range(0, len(self.detected) - 1):
			a = self.detected[i]
			for b in self.detected[i+1:]:
				a.connect(b)


	def overlaps(self, other, target):
		count = 0
		for a in self.detected:
			for b in other.detected:
				rotmap = a.overlaps(b, target)
				if rotmap is not None: # any one overlap is a win
					return rotmap
		return None


class Beacon:
	def __init__(self, position):
		self.position = position
		self.relative_positions = set() 

	def __str__(self):
		return str(self.position)

	def __repr__(self):
		return str(self.position)

	def __hash__(self):
		 return hash((self.position))

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.position == other.position)

	def connect(self, neighbor):
		self.relative_positions.add(neighbor.position - self.position)
		neighbor.relative_positions.add(self.position - neighbor.position)

	def print_positions(self):
		print self.position
		for relpos in self.relative_positions:
			print "  ", relpos
		print " "


	def overlaps(self, other, target):
		possibles = {}
		rotmaps = {}
		for a in self.relative_positions:
			for b in other.relative_positions:
				if a.similar(b):
					if a in possibles:
						print "U R SO EFFED", possibles[a], b
					rotmap = get_maps(a,b, self.position, other.position)
					if rotmap in rotmaps:
						rotmaps[rotmap] += 1
					else:
						rotmaps[rotmap] = 1
					possibles[a] = b
					# print rotmaps
					if rotmaps[rotmap] >= target - 1:  # -1 to include self
						btoa, atob = rotmap
						return (list(btoa), list(atob))


		# if len(possibles) > 0:
		# 	print "SCANNER", self.position, other.position, other.position.apply_map(rotmap[0])
		# 	print "  ROT", other.position.apply_rotation(rotmap[0])
		# 	print "  TRANS", other.position.apply_translation(rotmap[0])
		# 	for a, b in possibles.items():
		# 		print "  LOCAL", a, b, b.apply_rotation(rotmap[0])
		# for rotmap, count in rotmaps:
		# 	if count >= target - 1
		# if len(possibles) >= target - 1:
		# 	return rotmap
		return None


def get_flipper(a, b):
	return -1 if sign(a) != sign(b) else 1

def sign(val):
	return -1 if val < 0 else 1

def get_maps(a, b, aroot, broot):
	btoarot = a.get_mapping_func(b)
	btoa = (btoarot, aroot - broot.apply_rotation(btoarot))
	atobrot = b.get_mapping_func(a)
	atob = (atobrot, broot - aroot.apply_rotation(atobrot))

	return (btoa, atob)

def ctoa(ctob, btoa):
	return ctob + btoa

def testctoa(ctob, btoa, cpos):
	normal = cpos.apply_map(ctob).apply_map(btoa)
	combine = cpos.apply_map(ctoa(ctob, btoa))
	if normal == combine:
		return
	print "BIG ERROR", cpos, normal, combine 


pattern = r"((?P<x>.+),(?P<y>.+),(?P<z>.+)|--- scanner (?P<s>.+) ---)";

region = Region()
currentscanner = None
for line in file.readlines():
	if len(line.strip()) == 0:
		continue
	matches = re.match(pattern, line)
	data = matches.groupdict();
	s = data["s"]
	x = data["x"]
	y = data["y"]
	z = data["z"]

	if s is not None:
		if currentscanner is not None:
			region.addscanner(currentscanner)
		currentscanner = Scanner(int(s))
	elif x is not None:
		currentscanner.add(Beacon(Vector(int(x),int(y),int(z))))
	
target = 12
region.addscanner(currentscanner)
# print region.scanners[4].overlaps(region.scanners[1], target)
region.initmap()
# print region
result = region.get_highest_distance()

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)



