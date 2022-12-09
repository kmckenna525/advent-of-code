from timeit import default_timer as timer
import numpy as np

start = timer()
file = open('input.txt')

h = np.array([0,0])
t = np.array([0,0])

directions = {
	"L": np.array([-1,0]),
	"R": np.array([1,0]),
	"U": np.array([0,1]),
	"D": np.array([0,-1])
}

def should_follow(h, t):
	diff = np.absolute(h - t)
	return diff[0] > 1 or diff[1] > 1

def follow_vector(h, t):
	diff = h - t
	return np.clip(diff, -1, 1)


positions = set()
positions.add((0,0))
for line in file.readlines():
	[direction, amount] = line.strip().split()
	direction = directions[direction]
	amount = int(amount)

	for i in range(amount):
		h += direction
		if should_follow(h, t):
			t += follow_vector(h, t)
			positions.add((t[0], t[1]))

result = len(positions)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)