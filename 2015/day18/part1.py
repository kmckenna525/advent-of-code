from timeit import default_timer as timer

iterations = 5

start = timer()
file = open('input.txt')

# process input, 0 off # on
grid = []
for line in file.readlines():
	row = []
	for char in line:
		if char == "#":
			row.append(1)
		if char == ".":
			row.append(0)
	grid.append(row)

height = len(grid)
width = len(grid[0])
grid_copy = []
for i in range(0, height):
	grid_copy.append([0] * width)

def neighbors(rootx,rooty):
	for dirx in range(-1,2):
		for diry in range(-1,2):
			if dirx == 0 and diry == 0:
				continue
			x = dirx + rootx
			if x < 0 or x >= height:
				continue
			y = diry + rooty
			if y < 0 or y >= width:
				continue
			# print(x,y)
			yield grid[x][y]

def should_turn_off(x, y, target_min, target_max):
	total = 0
	for neighbor in neighbors(x,y):
		if neighbor == 1:
			total += 1
	return total < target_min or total > target_max

def should_turn_on(x, y, target):
	total = 0
	for neighbor in neighbors(x,y):
		if neighbor == 1:
			total += 1
	return total == target

def print_grid(grida):
	for x in range(0, height):
		row = ""
		for y in range(0, width):
			seat = grida[x][y]
			if seat == 0:
				row += "."
			if seat == 1:
				row += "#"
		print row
	print

def copy_grid(grida, gridb):
	for x in range(0, height):
		for y in range(0, width):
			grida[x][y] = gridb[x][y]

copy_grid(grid, grid)
copy_grid(grid_copy, grid)

# print_grid(grid)
# start the rules
for i in range(0, iterations):
	# run rules
	for x in range(0, height):
		for y in range(0, width):
			seat = grid[x][y]
			# check off
			if seat == 0 and should_turn_on(x,y, 3):
				grid_copy[x][y] = 1

			# check on
			if seat == 1 and should_turn_off(x,y, 2, 3):
				grid_copy[x][y] = 0

	copy_grid(grid, grid_copy)
	# print_grid(grid)

# count lights
result = 0
for x in range(0, height):
	for y in range(0, width):
		if grid[x][y] == 1:
			result += 1


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)