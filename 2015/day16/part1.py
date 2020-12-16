from timeit import default_timer as timer
import re

def parse_info(line):
	info = {}
	for item in line.split(", "):
		pair = item.split(": ")
		info[pair[0]] = int(pair[1])
	return info


start = timer()
file = open('input.txt')
lines = file.readlines()

target = parse_info(lines[0].strip())

def match(other):
	for (key, val) in other.items():
		if val != target[key]:
			return False
	return True

pattern = r"Sue (?P<id>\d+): (?P<list>.+)";
result = -1
for line in lines[1:]:
	matches = re.match(pattern, line.strip())
	data = matches.groupdict();
	sue = int(data["id"])
	info = parse_info(data["list"])
	if match(info):
		# print info
		result = sue

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)