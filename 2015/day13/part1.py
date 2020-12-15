from timeit import default_timer as timer
import re

class Node:
	def __init__(self, val):
		self.val = val
		self.neighbors = {}

	def __str__(self):
		return  "%s: %s" % (self.val, self.neighbors)

	def __repr__(self):
		return  self.val

	def connect(self, node, length):
		self.neighbors[node] = length

class Path:
	def __init__(self, existing):
		self.path = existing

	def __str__(self):
		return  " -> ".join(self.path)

	def __repr__(self):
		return  " -> ".join(self.path)

	def add(self, node):
		return Path(self.path + [node])

	def distance(self):
		if len(self.path) <= 1:
			return 0

		last = self.path[-1] 
		distance = 0
		for i in range(0, len(self.path)):
			node = self.path[i]
			distance += last.neighbors[node]
			distance += node.neighbors[last]
			last = node
		return distance

nodes = {}
def get_node(name):
	if name not in nodes:
		nodes[name] = Node(name)
	return nodes[name]


def get_paths(node, seen):
	paths = []
	seen.add(node)
	for (neighbor, distance) in node.neighbors.items():
		net = distance + neighbor.neighbors[node] # add the backlink
		if neighbor in seen:
			continue
		sub_paths = get_paths(neighbor, seen)
		for path in sub_paths:
			paths.append(path.add(node)) 
	seen.remove(node)
	if len(paths) == 0: # post base case lol
		paths.append(Path([node]))
	return paths

start = timer()
file = open('input.txt')

# process the nodes into a graph
pattern = r"(?P<a>\w+) would (?P<sign>gain|lose) (?P<distance>\d+) happiness units by sitting next to (?P<b>\w+)";
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	
	a = data["a"]
	b = data["b"]
	distance = int(data["distance"])
	distance = -distance if data["sign"] == "lose" else distance

	get_node(a).connect(get_node(b), distance)

# search paths
seen = set()
longest = None
for (name, node) in nodes.items():
	paths = get_paths(node, seen)
	for path in paths:
		# print (path, distance)
		distance = path.distance()
		if longest is None or distance > longest:
			longest = distance

result = longest

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)