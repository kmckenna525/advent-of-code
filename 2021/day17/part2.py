from timeit import default_timer as timer
import re
import math

start = timer()
file = open('input.txt')

class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return  "%d,%d" % (self.x, self.y)

	def __repr__(self):
		return  "%d,%d" % (self.x, self.y)

	def __hash__(self):
		 return hash((self.x, self.y))

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.x == other.x and
			self.y == other.y
		)

	def neg(self, other):
		return Vector(-self.x, -self.y)

	def sadd(self, scalar):
		return Vector(self.x + scalar, self.y + scalar)

	def smultiply(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)

	def add(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def multiply(self, other):
		return Vector(self.x * other.x, self.y * other.y)


pattern = r"target area: x=(?P<xmin>.+)\.\.(?P<xmax>.+), y=(?P<ymin>.+)\.\.(?P<ymax>.+)";
matches = re.match(pattern, file.read().strip())
data = matches.groupdict();
ymin = int(data["ymin"])
ymax = int(data["ymax"])
xmin = int(data["xmin"])
xmax = int(data["xmax"])


def binomial(val):
	return (val * (val + 1)) / 2


def starting(val): # approx inverse binomial?
	return int(math.sqrt(val * 2))


def binomialstep(val, t, bounded = False):
	if t > val and bounded:
		return binomial(val)
	return binomial(val) - binomial(val - t)


def sign(val):
	return -1 if val < 0 else 1


def pt(initial, t):
	return Vector(binomialstep(initial.x, t, True), binomialstep(initial.y, t, False))


def velocity(initial, t, bounded = False):
	if bounded:
		if t > abs(initial):
			return 0
		return (abs(initial) - t) * sign(initial)
	return inital - t


def inrange(position):
	return (
		position.x <= xmax and
		position.x >= xmin and
		position.y <= ymax and
		position.y >= ymin)


def afterrange(position):
	return (
		position.x > xmax and
		position.y < ymin)


def isshort(velocity): 
	return binomial(velocity.x) < xmin


def does_reach_target(velocity):
	if isshort(velocity):
		return False
	step = 1
	position = Vector(0,0)
	while position.x <= xmax and position.y >= ymin:
		position = pt(velocity, step)
		if inrange(position):
			return True
		if afterrange(position):
			return False
		step += 1

	return False


def maxvy(vx):
	if vx > xmax:
		return (vx/2) + 1 # make this vx if it doesn't work
	return ymin * -1


result = 0
minvx = starting(xmin)
maxvx = xmax + 1
for vx in range(minvx, maxvx):
	for vy in range(ymin, maxvy(vx)):
		velocity = Vector(vx, vy)

		if does_reach_target(velocity):
			result += 1
			# print velocity


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)