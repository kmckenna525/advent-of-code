from timeit import default_timer as timer

start = timer()
file = open('input.txt')

def is_visible_left(grid, x, y):
	height = grid[y][x]
	x -= 1
	while x >= 0:
		if grid[y][x] >= height:
			return False
		x -= 1
	return True

def is_visible_right(grid, x, y):
	height = grid[y][x]
	x += 1
	while x < len(grid[y]):
		if grid[y][x] >= height:
			return False
		x += 1
	return True

def is_visible_up(grid, x, y):
	height = grid[y][x]
	y -= 1
	while y >= 0:
		if grid[y][x] >= height:
			return False
		y -= 1
	return True

def is_visible_down(grid, x, y):
	height = grid[y][x]
	y += 1
	while y < len(grid):
		if grid[y][x] >= height:
			return False
		y += 1
	return True

def is_visible(grid, x, y):
	if x == 0 or y == 0:
		return True
	if y == len(grid) - 1 or x == len(grid[y]) - 1:
		return True

	# begin checking to the edges
	return is_visible_left(grid, x, y) or is_visible_right(grid, x, y) or is_visible_up(grid, x, y) or is_visible_down(grid, x, y)

grid = []
for line in file.readlines():
	grid.append([])
	for digit in line.strip():
		grid[-1].append(int(digit))
file.close()

result = 0
for y in range(len(grid)):
	for x in range(len(grid[0])):
		if is_visible(grid, x, y):
			result += 1


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)