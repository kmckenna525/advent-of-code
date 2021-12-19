from timeit import default_timer as timer
import re

class Node:
	def __init__(self, val):
		self.val = val
		self.children = set()

	def __str__(self):
		return  "%d" % (self.val)

	def __repr__(self):
		return str(self.val)

	def __hash__(self):
		 return hash((self.val))

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.val == other.val)


	def __getitem__(self, key):
		return None


	def __setitem__(self, key, value):
		return 

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