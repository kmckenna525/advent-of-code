from timeit import default_timer as timer
import math

# This assumes height == width of inputs. Some parts will still work for rectangles, but some will break

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
NUM_ORIENTATIONS = 4

def create_matrix(h,w, default = None):
	matrix = []
	for i in range(0, h):
		matrix.append([default] * w)
	return matrix


def orientations():
	for orientation in range(0, NUM_ORIENTATIONS):
		yield orientation

def rekey(flipped, orientation, target):
	if flipped:
		if target == NORTH:
			return orientation
		if target == EAST:
			return (WEST + orientation) % NUM_ORIENTATIONS
		if target == SOUTH:
			return (SOUTH + orientation) % NUM_ORIENTATIONS
		if target == WEST:
			return (EAST + orientation) % NUM_ORIENTATIONS
	return (target + orientation) % NUM_ORIENTATIONS

class Grid:
	def __init__(self, name):
		self.name = name
		self.grid = []
		self.orientation = NORTH
		self.flipped = False
		self.right = None
		self.left = None
		self.up = None
		self.down = None

	def __str__(self):
		return  "[%s, f:%s, o:%d]" % (self.name, self.flipped, self.orientation)

	def __repr__(self):
		# return  "[%s: %d x %d]" % (self.name, self.height, self.width)
		return  "%s" % (self.name)

	@property
	def height(self):
		return len(self.grid)

	@property
	def width(self):
		if self.height == 0:
			return 0
		return len(self.grid[0])

	@property
	def edges(self):
		for orientation in orientations():
			yield (orientation, self.get_edge(orientation))

	@staticmethod
	def edge_match(a, b):
		i = 0
		for val in b: # do this so b can be a generator
			if a[i] != val:
				return False
			i += 1
		return len(a) == i

	@staticmethod
	def parse_row(line):
		return list(line)
	
	def add_row(self, line):
		self.grid.append(self.parse_row(line))

	def get_column(self, i):
		col = []
		for y in range(0, self.height):
			col.append(self.grid[y][i])
		return col

	def rekey(self, ori):
		return rekey(self.flipped, self.orientation, ori)

	def get_edge(self, ori):
		if ori == NORTH:
			return self.grid[0]
		if ori == EAST:
			return self.get_column(self.width - 1)
		if ori == SOUTH:
			return self.grid[self.height - 1][::-1]
		if ori == WEST:
			return self.get_column(0)[::-1]
		return None


	def orient(self, side, expected):
		if self.flipped:
			for ori in orientations():
				if rekey(self.flipped, ori, side) == expected:
					self.orientation = ori
					return ori

		self.orientation = (side - expected) % NUM_ORIENTATIONS
		return self.orientation



	def flip(self):
		self.flipped = not self.flipped	


	def find_edges(self, edge):
		for orientation in orientations():
			if Grid.edge_match(self.get_edge(orientation), edge):
				yield (orientation, True)
			if Grid.edge_match(self.get_edge(orientation), reversed(edge)):
				yield (orientation, False)

	def connect_right(self, other):
		self.right = other
		other.left = self

	def connect_left(self, other):
		self.left = other
		other.right = self

	def connect_up(self, other):
		self.up = other
		other.down = self

	def connect_down(self, other):
		self.down = other
		other.up = self

	def remap_index(self, y, x):
		if self.flipped:
			x = -1 -x
		if self.orientation == NORTH:
			return (y, x)
		elif self.orientation == EAST:
			return (x, -1-y)
		elif self.orientation == SOUTH:
			return (-1-y, -1-x)
		elif self.orientation == WEST:
			return (-1-x, y)

		print "UHHHHH"
		return (y, x)


	def get_lines(self):
		new = []
		for y in range(0, self.height):
			row = ""
			for x in range(0, self.width):
				(rey, rex) = self.remap_index(y, x)
				# print (y, x, rey, rex)
				row += self.grid[rey][rex]
			new.append(row)
		return new


	def get_lines_borderless(self):
		new = []
		for y in range(1, self.height-1):
			row = ""
			for x in range(1, self.width-1):
				(rey, rex) = self.remap_index(y, x)
				# print (y, x, rey, rex)
				row += self.grid[rey][rex]
			new.append(row)
		return new




start = timer()
file = open('input.txt')

tiles = {}
in_tile = None
for line in file.readlines():
	line = line.strip()
	if "Tile" in line:
		name = int(line.replace("Tile ", "").replace(":", ""))
		in_tile = Grid(name)
		tiles[name] = in_tile
		continue

	if line.strip() == "":
		in_tile = None
		continue

	if in_tile is None:
		continue

	in_tile.add_row(line)

def find_tile_matches(edge, ignore):
	for tile in tiles.values():
		if tile == ignore:
			continue
		for orientation in tile.find_edges(edge):
			yield (tile, orientation)

# preprocess tile edge matches
match_data = {}
match_counts = {}
corners = []
# borders = []
# middles = []
for tile in tiles.values():
	data = {}
	match_data[tile.name] = data
	for (ori, edge) in tile.edges:
		matches = list(find_tile_matches(edge, tile))
		if len(matches) > 0:
			data[ori] = matches[0]
	count = len(data)
	match_counts[tile.name] = count
	if count == 2:
		corners.append(tile)
	# elif count == 3:
	# 	borders.append(tile)
	# elif count == 4:
	# 	middles.append(tile)


result = 1
for tile in corners:
	result *= tile.name

# early result - corners are known already
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)

def find_missing(tile, data):
	missing = []
	for ori in orientations():
		ori = tile.rekey(ori)
		if ori not in data:
			missing.append(ori)
	return missing

def orient_corner(tile):
	expected = NORTH
	data = match_data[tile.name]
	ori = find_missing(tile, data)[-1]
	tile.orient(ori, expected)

def get_connection_data(placed, tile):
	data = match_data[tile.name]
	for (ori, match) in data.items():
		if match[0] == placed:
			return match
	return None

def orient_from_connection(placed_data, tile, expected):
	# print placed_data
	# print expected
	tile.orient(placed_data[1][0], expected)

def flip_connection(placed_data, placed, tile):
	if placed_data[1][1] != placed.flipped:
		# print "flipped"
		tile.flip()

seen = set()
oriented = set()
def connect_next_tiles(tile, depth = 0):
	if not tile or tile in seen:
		return
	# print
	# print tile
	seen.add(tile)
	data = match_data[tile.name]
	# print data
	ori = tile.rekey(EAST)
	if ori in data:
		other = data[ori][0]
		tile.connect_right(other)
		# print (tile, "right", tile.right)
		if other not in oriented:
			flip_connection(data[ori], tile, tile.right)
			orient_from_connection(data[ori], tile.right, WEST)
			oriented.add(tile.right)
			# connect_next_tiles(tile.right)
	ori = tile.rekey(SOUTH)
	if ori in data:
		other = data[ori][0]
		tile.connect_down(other)
		# print (tile, "down", tile.down)
		if other not in oriented:
			flip_connection(data[ori], tile, tile.down)
			match = orient_from_connection(data[ori], tile.down, NORTH)
			oriented.add(tile.down)
			# connect_next_tiles(tile.down)
	ori = tile.rekey(WEST)
	if ori in data:
		other = data[ori][0]
		tile.connect_left(other)
		# print (tile, "left", tile.left)
		if other not in oriented:
			flip_connection(data[ori], tile, tile.left)
			match = orient_from_connection(data[ori], tile.left, EAST)
			oriented.add(tile.left)
			# connect_next_tiles(tile.left)
	ori = tile.rekey(NORTH)
	if ori in data:
		other = data[ori][0]
		tile.connect_up(other)
		# print (tile, "up", tile.up)
		if other not in oriented:
			flip_connection(data[ori], tile, tile.up)
			match = orient_from_connection(data[ori], tile.up, SOUTH)
			oriented.add(tile.up)
			# connect_next_tiles(tile.up)

target_size = int(math.sqrt(len(tiles)))
result_grid = create_matrix(target_size, target_size)


head = corners[0]
# I think I support doing this arbitrarily recursively, but choosing to 
# simplify debugging by forcing it to be top left corner and going from there
# We can also fill out the resulting grid this way
# head.flipped = True
orient_corner(head)
oriented.add(head)
connect_next_tiles(head)

row = 0
col = 0
colhead = head
while colhead:
	rowhead = colhead
	col = 0
	# if rowhead in corners:
	# 	print (rowhead, row, col)
	while rowhead:
		connect_next_tiles(rowhead)
		result_grid[row][col] = rowhead.get_lines()
		# result_grid[row][col] = rowhead.get_lines_borderless()

		# if not rowhead.right and rowhead in corners:
			# print (rowhead, row, col)
		rowhead = rowhead.right
		col += 1
	colhead = colhead.down
	row += 1

# for tile in tiles.values():
# 	print (tile, tile.up, tile.right, tile.down, tile.left)

# set to top left
# while head.up:
# 	head = head.up
# while head.left:
# 	head = head.left


print

tilesize = len(result_grid[0][0])
for row in range(0, target_size):
	for line in range(0, tilesize):
		pline = ""
		for col in range(0, target_size):
			pline += result_grid[row][col][line] + " "
		print pline
	print





