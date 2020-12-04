from timeit import default_timer as timer
import re

right = 3
down = 1

start = timer()
file = open('input.txt')
lines = file.readlines();
elevation = len(lines)
wrap = len(lines[0].strip())

currentRight = 0
result = 0
for i in range(0, elevation, down):
	line = lines[i]

	if line[currentRight % wrap] == "#":
		result += 1
	currentRight += right

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)