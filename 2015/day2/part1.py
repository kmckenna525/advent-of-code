from timeit import default_timer as timer
import re

file = open('input.txt')

pattern = r"(?P<l>\d+)x(?P<w>\d+)x(?P<h>\d+)";
result = 0
start = timer()
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();

	l = int(data["l"])
	w = int(data["w"])
	h = int(data["h"])

	side1 = l * w
	side2 = l * h
	side3 = w * h

	result += 2 * side1 + 2 * side2 + 2 * side3 + min(side1, side2, side3)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d sqft" % result)