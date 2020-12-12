from timeit import default_timer as timer

class Position:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def __str__(self):
		return  "%d,%d" % (self.x, self.y)

	def __repr__(self):
		return  "%d,%d" % (self.x, self.y)

	def rotate(self, amt):
		amt = amt % 360
		if amt == 0:
			return 0
		x = self.x
		y = self.y
		if amt == 90:
			self.x = y
			self.y = -x
		if amt == 180:
			self.x = -x
			self.y = -y
		if amt == 270:
			self.x = -y
			self.y = x

	def move_toward(self, other, amt):
		self.x += other.x * amt
		self.y += other.y * amt


waypoint = Position(10,1)
pos = Position()

start = timer()
file = open('input.txt')

for line in file.readlines():
	line = line.strip()
	instruction = line[0]
	amt = int(line[1:])

	if instruction == "N":
		waypoint.y += amt
	elif instruction == "S":
		waypoint.y -= amt
	elif instruction == "E":
		waypoint.x += amt
	elif instruction == "W":
		waypoint.x -= amt
	elif instruction == "L":
		waypoint.rotate(-amt)
	elif instruction == "R":
		waypoint.rotate(amt)
	elif instruction == "F":
		pos.move_toward(waypoint, amt)
	
result = abs(pos.x) + abs(pos.y)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)