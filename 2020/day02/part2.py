from timeit import default_timer as timer
import re

file = open('input.txt')

pattern = r"(?P<pos1>\d+)-(?P<pos2>\d+) (?P<target>.): (?P<password>\w+)";
result = 0
start = timer()
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();

	pos1 = int(data["pos1"])
	pos2 = int(data["pos2"])
	target = data["target"]
	password = data["password"]

	has1 = password[pos1 - 1] == target
	has2 = password[pos2 - 1] == target
	if has1 != has2:
		result += 1

print("%d valid passwords" % result)
print("Completed in %fms" % ((timer() - start) * 1000))