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

	dims = [l,w,h]
	dims.sort()

	result += 2 * dims[0] + 2 * dims[1] + l * w * h

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d ft" % result)