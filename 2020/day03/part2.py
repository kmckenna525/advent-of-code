from timeit import default_timer as timer
import re

def countTrees(lines, right, down):
	elevation = len(lines)
	wrap = len(lines[0].strip())
	currentRight = 0
	result = 0
	for i in range(0, elevation, down):
		line = lines[i]

		if line[currentRight % wrap] == "#":
			result += 1
		currentRight += right
	return result

start = timer()
file = open('input.txt')
lines = file.readlines();

a = countTrees(lines, 1, 1)
b = countTrees(lines, 3, 1)
c = countTrees(lines, 5, 1)
d = countTrees(lines, 7, 1)
e = countTrees(lines, 1, 2)
result = a * b * c * d * e

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result (%d,%d,%d,%d,%d)" % (result, a, b, c, d, e))