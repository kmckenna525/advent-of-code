from timeit import default_timer as timer
import math

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

class Grid:
	def __init__(self, name):
		self.name = name
		self.grid = []
		self.orientation = NORTH
		self.is_mirrored_vert = False
		self.is_mirrored_horz = False
		self.right = None
		self.left = None
		self.up = None
		self.down = None

	def __str__(self):
		return  "[%s]" % (self.name)

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
		ori = (ori + self.orientation) % NUM_ORIENTATIONS
		if self.is_mirrored_vert and ori % 2 != 0:
			return (ori - 2) % NUM_ORIENTATIONS
		if self.is_mirrored_horz and ori % 2 == 0:
			return (ori - 2) % NUM_ORIENTATIONS
		return ori

	def unkey(self, ori):
		return (ori - self.orientation) % NUM_ORIENTATIONS

	def get_edge(self, ori):
		if ori == NORTH:
			return self.grid[0]
		if ori == EAST:
			return self.get_column(self.width - 1)
		if ori == SOUTH:
			return self.grid[self.height - 1]
		if ori == WEST:
			return self.get_column(0)
		return None


	def orient(self, new_orientation):
		self.orientation = new_orientation

	def mirror_vertical(self):
		self.is_mirrored_vert = not self.is_mirrored_vert
		# width = self.width
		# for y in range(0, self.height):
		# 	row = self.grid[y]
		# 	for x in range(0, int(width/2)):
		# 		temp = row[x]
		# 		other = width - x - 1
		# 		row[x] = row[other]
		# 		row[other] = temp

	def mirror_horizontal(self):
		self.is_mirrored_horz = not self.is_mirrored_horz
		# height = self.height
		# grid = self.grid
		# for y in range(0, height):
		# 	temp = grid[y]
		# 	other = height - y - 1
		# 	grid[y] = grid[other]
		# 	grid[other] = temp

	def find_edges(self, edge):
		for orientation in orientations():
			if Grid.edge_match(self.get_edge(orientation), edge):
				yield (orientation, False)
			if Grid.edge_match(self.get_edge(orientation), reversed(edge)):
				yield (orientation, True)

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
borders = []
middles = []
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
	elif count == 3:
		borders.append(tile)
	elif count == 4:
		middles.append(tile)


result = 1
for tile in corners:
	result *= tile.name

# early result - corners are known already
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)


def should_flip_vert(tile, data):
	north = tile.rekey(NORTH)
	south = tile.rekey(SOUTH)
	if north in data and south in data:
		return data[south][1][1] and data[north][1][1]
	if north not in data and south in data:
		return data[south][1][1]
	if north in data and south not in data:
		return data[north][1][1]
	return False

def should_flip_horz(tile, data):
	west = tile.rekey(WEST)
	east = tile.rekey(EAST)
	if east in data and west in data:
		return data[west][1][1] and data[east][1][1]
	if east not in data and west in data:
		return data[west][1][1]
	if east in data and west not in data:
		return data[east][1][1]
	return False

target_size = int(math.sqrt(len(tiles)))
last = target_size - 1
BORDER_Y = {
	0: NORTH,
	last: SOUTH
}
BORDER_X = {
	0: EAST,
	last: WEST
}
CORNERS = {
	(0,0): NORTH,
	(0, last): EAST,
	(last, last): SOUTH,
	(last, 0): WEST
}

result_grid = create_matrix(target_size, target_size)

def corner(x,y):
	return x in BORDER_X and x in BORDER_Y

def border(x,y):
	return x in BORDER_X or x in BORDER_Y

def has_up(x,y):
	return y > 0
def has_down(x,y):
	return y < last
def has_left(x,y):
	return x > 0
def has_right(x,y):
	return x < last

def orient_border(tile, x, y):
	expected = BORDER_X[x] if x in BORDER_X else BORDER_Y[y]
	data = match_data[tile.name]
	for ori in orientations:
		if ori not in data[ori]:
			tile.orient((ori - expected) % NUM_ORIENTATIONS)
			return

def find_second_missing(data):
	found = None
	for ori in orientations():
		if ori not in data:
			if found:
				return ori
			found = True
		elif found:
			return ori - 1

def orient_corner(tile, x, y):
	expected = CORNERS[(x,y)]
	data = match_data[tile.name]
	print data
	ori = find_second_missing(data)
	tile.orient((ori - expected) % NUM_ORIENTATIONS)

def get_connection_data(placed, tile):
	data = match_data[tile.name]
	for (ori, match) in data.items():
		if match[0] == placed:
			return match
	return None

def orient_from_connection(placed, tile, expected):
	data = match_data[tile.name]
	for (ori, match) in data.items():
		if match[0] == placed:
			tile.orient((ori - expected) % NUM_ORIENTATIONS)
			return 
	print "ERROR NO MATCHING MATCH FOR TILE"

def flip_if_needed(tile, x, y):
	if has_left(x,y):
		left = tile.left
		match = get_connection_data(left, tile)
		if match[1][1] and not left.is_mirrored_horz:
			print "flipped"
			tile.mirror_horizontal()
	elif has_up(x,y):
		up = tile.up
		match = get_connection_data(up, tile)
		if match[1][1] and not up.is_mirrored_vert:
			print "flipped"
			tile.mirror_vertical()

def connect_next_tiles(tile, x, y):
	data = match_data[tile.name]
	print data
	print tile.orientation
	if has_right(x,y):
		tile.connect_right(data[tile.rekey(EAST)][0])
	if has_down(x,y):
		tile.connect_down(data[tile.rekey(SOUTH)][0])


for y in range(0, target_size):
	for x in range(0, target_size):
		print (x,y)
		if x == 0 and y == 0:
			tile = corners.pop(0)
			print tile
			result_grid[y][x] = tile
			orient_corner(tile, x, y)
			connect_next_tiles(tile, x, y)
			data = match_data[tile.name]
			continue

		last_placement = None
		tile = None
		if has_left(x,y):
			print "got left right"
			last_placement = result_grid[y][x-1]
			tile = last_placement.right
			orient_from_connection(last_placement, tile, WEST)
		elif has_up(x,y):
			print "got up"
			last_placement = result_grid[y-1][x]
			tile = last_placement.down
			orient_from_connection(last_placement, tile, NORTH)
		else:
			print "WHAAAAT NOOOOO CONNECTION"
		result_grid[y][x] = tile
		print tile
		flip_if_needed(tile, x, y)
		connect_next_tiles(tile, x, y)








