from timeit import default_timer as timer
import re

class Node:
	def __init__(self, val):
		self.val = val
		self.children = set()

	def __str__(self):
		return  "%d" % (self.val)

	def __repr__(self):
		return  "%d" % (self.val)

	def connect(self, node):
		self.children.add(node)

start = timer()
file = open('input.txt')

pattern = r"(?P<group>\w+)";
result = 0
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	group = data["group"]
	
	result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)