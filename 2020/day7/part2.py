from timeit import default_timer as timer
import re

class Node:
	def __init__(self, node_type):
		self.node_type = node_type
		self.children = {}
		self.parents = set()

	def __str__(self):
		return  "%s: %s" % (self.node_type, self.children)

	def __repr__(self):
		return  self.node_type

	def add_child(self, node, amt):
		self.children[node] = amt
		node.parents.add(self)

class NodeGraph:
	def __init__(self):
		self.heads = set()
		self.nodes = {}

	def get_or_add(self, node_type):
		node = None
		if node_type in self.nodes:
			node = self.nodes[node_type]
		else:
			node = Node(node_type)
			self.nodes[node_type] = node
			self.heads.add(node)
		return node

	def add_child(self, node_type, child_type, amt):
		node = self.get_or_add(node_type)
		sub_node = self.get_or_add(child_type)

		node.add_child(sub_node, amt)
		if sub_node in self.heads:
			self.heads.remove(sub_node)


def count_children(node):
	if len(node.children) == 0:
		return 0

	# print node
	count = 0
	for (child, amt) in node.children.items():
		# print(child, amt)
		count += amt + amt * count_children(child)
	return count

start = timer()
file = open('input.txt')

pattern = r"(?P<main>.+) bags contain (?P<rest>.+)";
bag=r"(?P<sub_amt>\d+) (?P<sub_type>.+) bag"

graph = NodeGraph()
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	main = data["main"]
	rest = data["rest"]

	graph.get_or_add(main)

	# print("%s (%s)"%(main, rest))
	for rule in rest.split(","):
		if rule == "no other bags.":
			continue
		
		matches = re.search(bag, rule)

		if not matches:
			print("possible error %s"%rule)
			continue

		data = matches.groupdict();
		sub_amt = int(data["sub_amt"])
		sub_type = data["sub_type"]

		graph.add_child(main, sub_type, sub_amt)
		# print("%d %s"%(sub_amt, sub_type))

node = graph.get_or_add("shiny gold")
result = count_children(node)


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)
# print(results)