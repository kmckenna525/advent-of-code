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
		node.neighbors[self] = length

nodes = {}
def get_node(city):
	if city not in nodes:
		nodes[city] = Node(city)
	return nodes[city]


def get_paths(node, seen):
	paths = []
	seen.add(node)
	for (neighbor, distance) in node.neighbors.items():
		if neighbor in seen:
			continue
		sub_paths = get_paths(neighbor, seen)
		for (path, path_distance) in sub_paths:
			paths.append((node.val + " -> " + path, distance + path_distance)) 
	seen.remove(node)
	if len(paths) == 0: # post base case lol
		paths.append((node.val, 0))
	return paths

start = timer()
file = open('input.txt')

# process the nodes into a graph
pattern = r"(?P<a>.+) to (?P<b>.+) = (?P<distance>\d+)";
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	
	a = data["a"]
	b = data["b"]
	distance = int(data["distance"])

	get_node(a).connect(get_node(b), distance)

# search paths
seen = set()
longest = None
for (city, node) in nodes.items():
	paths = get_paths(node, seen)
	for (path, distance) in paths:
		# print (path, distance)
		if longest is None or distance > longest:
			longest = distance

result = longest

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)