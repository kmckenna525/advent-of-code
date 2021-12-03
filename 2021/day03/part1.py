from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

lines = file.readlines()
bitcount = len(lines[0].strip())
counts0 = [0] * bitcount
counts1 = [0] * bitcount
for line in lines:
	binarynum = line.strip()

	i = 0
	for val in binarynum:
		if val == "0":
			counts0[i] += 1
		if val == "1":
			counts1[i] += 1
		i += 1

gamma = ""
epsilon = ""
for i in range(0, bitcount):
	if counts1[i] > counts0[i]:
		gamma += "1"
		epsilon += "0"
	else:
		gamma += "0"
		epsilon += "1"

gamma = int(gamma, 2)
epsilon = int(epsilon, 2)
result = gamma * epsilon

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d, %d: %d is the result" % (gamma, epsilon, result))