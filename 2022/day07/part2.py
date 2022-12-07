from timeit import default_timer as timer

start = timer()
file = open('input.txt')

class Node:
	def __init__(self, parent, name, size = 0):
		self.parent = parent
		self.is_dir = size == 0
		self.name = name
		self.size = size
		self.children = []

	def __str__(self):
		return  "%s (%d)" % (self.name, self.size)

	def __repr__(self):
		return  "%s (%d)" % (self.name, self.size)

	def add(self, name, size = 0):
		self.children.append(Node(self, name, size))

	def calclate_size(self):
		if not self.is_dir:
			return self.size

		self.size = 0;
		for child in self.children:
			child.calclate_size()
			self.size += child.size
		return self.size

	def __getitem__(self, key):
		for child in self.children:
			if child.name == key:
				return child

	def recurse_dirs(self):
		yield self
		for child in self.children:
			if child.is_dir:
				for subchild in child.recurse_dirs():
					yield subchild


total_space = 70000000
needed = 30000000

root = Node(None, "/")
current = root
for line in file.readlines():
	parts = line.strip().split()
	if line.startswith("$ cd"):
		name = parts[2]
		if name == "/":
			current = root
		elif name == "..":
			current = current.parent
		else:
			current = current[name]

	elif line.startswith("$ ls"):
		continue

	elif parts[0] == "dir":
		current.add(parts[1])
	else:
		current.add(parts[1], int(parts[0]))
file.close()

left = total_space - root.calclate_size()
min_size = needed - left
print root.size

result = root.size
for directory in root.recurse_dirs():
	if directory.size >= min_size and directory.size < result:
		result = directory.size


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)