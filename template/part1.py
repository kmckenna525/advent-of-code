from timeit import default_timer as timer
import re

start = timer()

pattern = r"(?P<group>\w+)";
result = 0
with open('input.txt') as file:
	for line in file.readlines():
		matches = re.match(pattern, line)
		data = matches.groupdict();
		group = data["group"]
		
		result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)