from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

pattern = r"(-?\d+)"
result = 0
for line in file.readlines():
	matches = re.findall(pattern, line)
	for match in matches:
		result += int(match)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)