from timeit import default_timer as timer
import re

file = open('input.txt')

pattern = r"(?P<min>\d+)-(?P<max>\d+) (?P<target>.): (?P<password>\w+)";
result = 0
start = timer()
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();

	min = int(data["min"])
	max = int(data["max"])
	target = data["target"]
	password = data["password"]

	count = 0;
	for char in password:
		if char == target:
			count+=1

	if count >= min and count <= max:
		result+=1

print("%d valid passwords" % result)
print("Completed in %fms" % ((timer() - start) * 1000))