from timeit import default_timer as timer

degrees = {
	0: "E",
	90: "S",
	180: "W",
	270: "N"
}

class Position:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.facing = 0

	def __str__(self):
		return  "%d,%d (%d)" % (self.x, self.y, self.facing)

	def __repr__(self):
		return  "%d,%d (%d)" % (self.x, self.y, self.facing)

	def rotate(self, amt):
		self.facing = (self.facing + amt) % 360

pos = Position()

def move(instruction, amt):
	if instruction == "N":
		pos.y += amt
	elif instruction == "S":
		pos.y -= amt
	elif instruction == "E":
		pos.x += amt
	elif instruction == "W":
		pos.x -= amt
	elif instruction == "L":
		pos.rotate(-amt)
	elif instruction == "R":
		pos.rotate(amt)
	elif instruction == "F":
		move(degrees[pos.facing], amt)

start = timer()
file = open('input.txt')

for line in file.readlines():
	line = line.strip()
	instruction = line[0]
	amt = int(line[1:])

	move(instruction, amt)
	
result = abs(pos.x) + abs(pos.y)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)