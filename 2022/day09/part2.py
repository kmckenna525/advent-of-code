from timeit import default_timer as timer
import numpy as np

start = timer()
file = open('input.txt')

rope = []
for i in range(10):
	rope.append(np.array([0,0]))

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


positions = set() # don't need to add 0,0 since we add tpos every iteration now
for line in file.readlines():
	[direction, amount] = line.strip().split()
	direction = directions[direction]
	amount = int(amount)

	for i in range(amount):
		rope[0] += direction
		for i in range(1, len(rope)):
			if not should_follow(rope[i - 1], rope[i]):
				break

			rope[i] += follow_vector(rope[i - 1], rope[i])
		tpos = (rope[-1][0], rope[-1][1])
		positions.add(tpos)

result = len(positions)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)