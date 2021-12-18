from timeit import default_timer as timer
import json
import math

start = timer()
file = open('input.txt')

verbose = False

class Node:
	def __init__(self, val = None, left = None, right = None, parent = None):
		self.val = val 
		self.parent = parent
		self.left = left
		self.right = right

	def __str__(self):
		if self.isleaf:
			return str(self.val)
		return  "[%s,%s]" % (str(self.left), str(self.right))

	def __repr__(self):
		if self.isleaf:
			return str(self.val)
		return  "[%s,%s]" % (str(self.left), str(self.right))

	@property
	def isleft(self):
		if self.parent is None:
			return False
		return self.parent.left == self

	@property
	def isright(self):
		if self.parent is None:
			return False
		return self.parent.right == self

	@property
	def isleaf(self):
		return self.left is None and self.right is None

	@property
	def isroot(self):
		return self.parent is None
	


def map(val, parent = None):
	if type(val) is int:
		return Node(val, parent = parent)

	node = Node(parent = parent)
	node.left = map(val[0], node)
	node.right = map(val[1], node)
	return node


def magnitude(pair):
	if pair.isleaf:
		return pair.val
	return (magnitude(pair.left) * 3) + (magnitude(pair.right) * 2)

#[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
def add(pair1, pair2):
	pair = Node(left = pair1, right = pair2)
	pair1.parent = pair
	pair2.parent = pair
	if verbose:
		print "ADDED", pair
	return reduce(pair)

def reduce(pair):
	stack = []
	current = pair
	depth = 0
	# apply any explodes
	while current is not None or len(stack) > 0:
		# load up this branch
		while current is not None:
			stack.append((current, depth))

			current = current.left # set to left
			depth += 1

		current, depth = stack.pop()

		# check for explode
		if not current.isleaf and depth >= 4:
			explode(current)
			if verbose:
				print pair
			# reset to root
			return reduce(pair)

		# do my right babies next
		current = current.right
		depth += 1

	# apply splits if no explodes
	current = pair
	while current is not None or len(stack) > 0:
		# load up this branch
		while current is not None:
			stack.append((current, depth))

			current = current.left # set to left

		current, depth = stack.pop()

		if current.isleaf and current.val >= 10:
			split(current)
			if verbose:
				print pair
			# reset to root
			return reduce(pair)

		# do my right babies next
		current = current.right

	return pair

def explode(pair):
	if verbose:
		print "EXPLODE", pair
	left = left_leaf(pair.left)
	if left is not None:
		left.val += pair.left.val
	right = right_leaf(pair.right)
	if right is not None:
		right.val += pair.right.val
	pair.val = 0
	pair.left = None
	pair.right = None
	

def split(leaf):
	if verbose:
		print "SPLIT", leaf
	half = leaf.val/2.0
	leaf.left = Node(int(math.floor(half)), parent = leaf)
	leaf.right = Node(int(math.ceil(half)), parent = leaf)
	leaf.val = None


def left_leaf(leaf):
	# find first parent that is not a left node
	node = leaf
	while node is not None and node.isleft:
		node = node.parent

	if node is None or node.isroot:
		if verbose:
			print "no left"
		return None # we are leftmost already
	
	# use the left sibling of the node we found
	left = node.parent.left

	while left.right is not None: # fast forward to rightmost leaf of left sibling
		left = left.right

	if verbose:
		print "left", left
	return left

def right_leaf(leaf):
	# find first parent that is not a right node
	node = leaf
	while node is not None and node.isright:
		node = node.parent

	if node is None or node.isroot:
		if verbose:
			print "no right"
		return None # we are rightmost already
	
	# use the right sibling of the node we found
	right = node.parent.right

	while right.left is not None: # fast forward to leftmost leaf of right sibling
		right = right.left

	if verbose:
		print "right", right
	return right


pairs = []
for line in file.readlines():
	pair = map(json.loads(line.strip()))
	pairs.append(pair)


total = pairs[0]
for pair in pairs[1:]:
	total = add(total, pair)
	if verbose:
		print "TOTAL", total


result = magnitude(total)
print("Completed in %fms" % ((timer() - start) * 1000))
print(total)
print("%d is the result" % result)