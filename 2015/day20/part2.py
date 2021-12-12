from timeit import default_timer as timer
import re
import math

start = timer()
file = open('input.txt')

target = int(file.read().strip())
multiplier = 11
maxval = (target/multiplier)
maxdeliveries = 50
houses = [0] * maxval

for elfnum in range(1, maxval):
	for i in range(0, maxdeliveries):
		housenum = elfnum * (i + 1)
		if housenum > maxval:
			break
		houses[housenum] += elfnum * multiplier

result = -1
for i in range(1,maxval):
	# print "House %d got %d presents." % (i, houses[i])
	if houses[i] >= target:
		result = i
		break

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)