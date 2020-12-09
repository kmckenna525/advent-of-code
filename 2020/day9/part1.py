from timeit import default_timer as timer
from collections import deque

preamble_len = 25

start = timer()
file = open('input.txt')

queue = deque()

def validate(val):
	for x in queue:
		for y in queue:
			if x == y:
				continue
			if x + y == val:
				return True
	return False

result = -1
for line in file.readlines():
	num = int(line)

	if len(queue) >= preamble_len:
		if(not validate(num)):
			result = num
			break
		queue.popleft()

	queue.append(num)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)