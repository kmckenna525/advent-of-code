from timeit import default_timer as timer
import re

height = 1000
width = 1000
matrix = [0] * width * height

def key(x,y):
	return y * width + x

def toggle(start, end):
	for x in range(start[0], end[0] + 1):
		for y in range(start[1], end[1] + 1):
			matrix[key(x,y)] += 2

def turn_off(start, end):
	for x in range(start[0], end[0] + 1):
		for y in range(start[1], end[1] + 1):
			if matrix[key(x,y)] == 0:
				continue
			matrix[key(x,y)] -= 1

def turn_on(start, end):
	for x in range(start[0], end[0] + 1):
		for y in range(start[1], end[1] + 1):
			matrix[key(x,y)] += 1

commands = {
	"toggle": toggle,
	"turn on": turn_on,
	"turn off": turn_off
}

start = timer()
file = open('input.txt')

pattern = r"(?P<command>toggle|turn on|turn off) (?P<startx>\d+),(?P<starty>\d+) through (?P<endx>\d+),(?P<endy>\d+)";

for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	command = data["command"]
	startx = int(data["startx"])
	starty = int(data["starty"])
	endx = int(data["endx"])
	endy = int(data["endy"])

	commands[command]((startx,starty), (endx,endy))
	
result = 0
for val in matrix:
	result += val

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)