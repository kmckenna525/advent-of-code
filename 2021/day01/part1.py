from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

prev = None
result = 0
for line in file.readlines():
	num = int(line.strip())
	if prev is None:
		#initing
		prev = num
		continue

	if num > prev:
		result += 1

	prev = num

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)