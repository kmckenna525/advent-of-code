from timeit import default_timer as timer

start = timer()
file = open('input.txt')

def count_left(grid, x, y):
	height = grid[y][x]
	count = 0
	while x - count - 1 >= 0:
		count += 1
		if grid[y][x-count] >= height:
			return count
	return count

def count_right(grid, x, y):
	height = grid[y][x]
	count = 0
	while x + count + 1 < len(grid[y]):
		count += 1
		if grid[y][x + count] >= height:
			return count
	return count

def count_up(grid, x, y):
	height = grid[y][x]
	count = 0
	while y - count - 1 >= 0:
		count += 1
		if grid[y - count][x] >= height:
			return count
	return count

def count_down(grid, x, y):
	height = grid[y][x]
	count = 0
	while y + count + 1 < len(grid):
		count += 1
		if grid[y + count][x] >= height:
			return count
	return count

def get_score(grid, x, y):
	if x == 0 or y == 0:
		return 0
	if y == len(grid) - 1 or x == len(grid[y]) - 1:
		return 0

	left = count_left(grid, x, y)
	right = count_right(grid, x, y)
	up = count_up(grid, x, y)
	down = count_down(grid, x, y)

	# print(x, y, grid[y][x], left, right, up, down)

	# begin checking to the edges
	return left * right * up * down

grid = []
for line in file.readlines():
	grid.append([])
	for digit in line.strip():
		grid[-1].append(int(digit))
file.close()

result = 0
for y in range(len(grid)):
	for x in range(len(grid[0])):
		score = get_score(grid, x, y)
		# print (x,y,score)
		if score > result:
			result = score


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)