from timeit import default_timer as timer

start = timer()
file = open('input.txt')

# process input, 0 floor, 1 empty, 2 taken
grid = []
for line in file.readlines():
	row = []
	for char in line:
		if char == "#":
			row.append(2)
		if char == "L":
			row.append(1)
		if char == ".":
			row.append(0)
	grid.append(row)

height = len(grid)
width = len(grid[0])
grid_copy = []
for i in range(0, height):
	grid_copy.append([0] * width)

def is_valid(x,y):
	if x < 0 or x >= height:
		return False
	if y < 0 or y >= width:
		return False
	return True

def neighbors(rootx,rooty):
	for dirx in range(-1,2):
		for diry in range(-1,2):
			if dirx == 0 and diry == 0:
				continue
			x = dirx + rootx
			y = diry + rooty
			while is_valid(x,y):
				if grid[x][y] > 0:
					yield grid[x][y]
					break
				x += dirx
				y += diry

def all_empty(x, y):
	for neighbor in neighbors(x,y):
		if neighbor == 2:
			return False
	return True

def too_many(x, y, max_taken):
	total = 0
	for neighbor in neighbors(x,y):
		if neighbor == 2:
			total += 1
		if total >= max_taken:
			return True
	return False

def print_grid(grida):
	for x in range(0, height):
		row = ""
		for y in range(0, width):
			seat = grida[x][y]
			if seat == 0:
				row += "."
			if seat == 1:
				row += "L"
			if seat == 2:
				row += "#"
		print row
	print

def copy_grid(grida, gridb):
	for x in range(0, height):
		for y in range(0, width):
			grida[x][y] = gridb[x][y]

copy_grid(grid_copy, grid)

# start the rules
count = 0
did_change = True
while(did_change):
	count += 1
	did_change = False

	# run rules
	for x in range(0, height):
		for y in range(0, width):
			seat = grid[x][y]
			if seat == 0:
				continue

			# check empty
			if seat == 1 and all_empty(x,y):
				grid_copy[x][y] = 2
				did_change = True

			# check surrounded by >= 5
			if seat == 2 and too_many(x,y, 5):
				grid_copy[x][y] = 1
				did_change = True

	copy_grid(grid, grid_copy)
	# print_grid(grid)

# count seats
result = 0
for x in range(0, height):
	for y in range(0, width):
		if grid[x][y] == 2:
			result += 1


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)