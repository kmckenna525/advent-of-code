from timeit import default_timer as timer
import re

tstart = timer()
file = open('input.txt')

class Node:
	def __init__(self, val):
		self.val = val
		self.connections = set()

	def __str__(self):
		return  "%s" % (self.val)

	def __repr__(self):
		return  "%s" % (self.val)

	@property
	def issmall(self):
		return self.val.islower()
	

	def connect(self, node):
		self.connections.add(node)
		node.connections.add(self)


graph = {}
def get_node(val):
	if val not in graph:
		graph[val] = Node(val)
	
	return graph[val]


def find_paths(start, prefix, end, seen_smalls):
	prefix = prefix + "," + start.val
	if start == end:
		return set([prefix])

	paths = set()
	for node in start.connections:
		if node.issmall:
			if node in seen_smalls:
				continue
			seen_smalls.add(node)
		paths.update(find_paths(node, prefix, end, seen_smalls))
		if node.issmall:
			seen_smalls.remove(node)

	return paths


start = None
end = None

pattern = r"(?P<beg>\w+)-(?P<to>\w+)";
for line in file.readlines():
	matches = re.match(pattern, line.strip())
	data = matches.groupdict();
	beg = data["beg"]
	to = data["to"]

	begnode = get_node(beg)
	tonode = get_node(to)
	begnode.connect(tonode)

	if beg == "start":
		start = begnode
	if to == "end":
		end = tonode



paths = find_paths(start, "", end, set([start]))
# for path in paths:
# 	print path
result = len(paths)
print("Completed in %fms" % ((timer() - tstart) * 1000))
print("%d is the result" % result)