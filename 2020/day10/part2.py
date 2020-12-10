from timeit import default_timer as timer
from collections import deque

class Node:
	def __init__(self, val):
		self.val = val
		self.children = set()

	def __str__(self):
		return  "%s: %s" % (self.val, self.children)

	def __repr__(self):
		return  self.val

	def connect(self, node):
		self.children.add(node)

memo = {}
def dfs(node):
	if len(node.children) == 0:
		return 1

	if node in memo:
		return memo[node]

	paths = 0
	for child in node.children:
		paths += dfs(child)
	memo[node] = paths
	return paths


start = timer()
file = open('input.txt')

# pre process input
values = []
for line in file.readlines():
	values.append(int(line))
values.sort()
values.append(values[-1] + 3)


# construct directed graph
head = Node(0)
prev = deque([head])
for val in values:
	node = Node(val)
	while(prev[0].val + 3 < val):
		# print("%d + 3 < %d" % (prev[0].val, val))
		prev.popleft()
	for other in prev:
		# print ("connect %d -> %d" % (other.val, val))
		other.connect(node)
	prev.append(node)

#dfs
result = dfs(head)


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)