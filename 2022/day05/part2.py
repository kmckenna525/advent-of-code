from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

pattern = r"move (?P<num>\d+) from (?P<src>\d+) to (?P<dst>\d+)"
result = 0

is_moves = False
grid = None
for line in file.readlines():
	if is_moves:
		# grid is [[top, .., bottom]]

		matches = re.match(pattern, line)
		data = matches.groupdict();
		num = int(data["num"])
		src = int(data["src"]) - 1
		dst = int(data["dst"]) - 1

		for i in reversed(range(num)):
			item = grid[src].pop(i)
			grid[dst].insert(0, item)

		# print("move", num, src, dst)
		# print(grid)

		continue

	if len(line.strip()) == 0:
		is_moves = True
		continue
	if line[1] == "1":
		continue

	columns = list([ line[i] for i in range(1, len(line), 4) ])
	if grid is None:
		grid = []
		for column in columns:
			grid.append([])

	for i in range(len(columns)):
		column = columns[i]
		if column == ' ':
			continue
		grid[i].append(column)
	
	result += 1
# print grid

result = ''.join([stack[0] for stack in grid])

print("Completed in %fms" % ((timer() - start) * 1000))
print("%s is the result" % result)