from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

target = int(file.read().strip())
multiplier = 10
maxval = (target/multiplier)
houses = [0] * maxval

for elfnum in range(1, maxval):
	for housenum in range(elfnum, maxval, elfnum):
		houses[housenum] += elfnum * multiplier

result = -1
for i in range(1,maxval):
	# print "House %d got %d presents." % (i, houses[i])
	if houses[i] >= target:
		result = i
		break

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)