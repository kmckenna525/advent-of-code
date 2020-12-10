from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

pair = r"(..).*\1"
repeat = r"(.).\1"

result = 0
for line in file.readlines():
	trimmed = line.strip()

	if not re.search(pair, trimmed):
		# print("no repeating pair", trimmed)
		continue
	if not re.search(repeat, trimmed):
		# print("failed to find aba pattern", trimmed)
		continue
	
	result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)