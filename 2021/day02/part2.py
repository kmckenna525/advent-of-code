from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

pattern = r"(?P<direction>\w+) (?P<amt>\d+)";
position = 0
depth = 0
aim = 0
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	direction = data["direction"]
	amt = int(data["amt"])

	if direction == "forward":
		position += amt
		depth += aim * amt
	elif direction == "up":
		aim -= amt
	elif direction == "down":
		aim += amt

result = position * depth
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d, %d, %d and %d is the result" % (position, depth, aim, result))