from timeit import default_timer as timer

class EquationNode:
	def __init__(self, parent = None):
		self.parent = parent
		self.left = None
		self.right = None
		self.operator = None

	def evaluate(self):
		left = self.left
		right = self.right

		if right is None:
			print ("invalid right???")
			return 0

		if not isinstance(right, int):
			right = right.evaluate()

		if left is None:
			# print ("%d"%(right))
			return right

		if not isinstance(left, int):
			left = left.evaluate()

		if self.operator == "+":
			# print ("%d + %d"%(left, right))
			return left + right
		if self.operator == "*":
			# print ("%d * %d"%(left, right))
			return left * right
		
		print ("invalid operator??? %s" % self.operator)
		return -1

def tryParseInt(token):
	try:
		return int(token)
	except:
		return None


class Tokenizer:
	# 0 expect number or group
	# 1 expect operator
	def __init__(self):
		self.state = 0
		self.depth = 0
		self.curr = EquationNode()
		self.head = self.curr

	def parse(self, token):
		if token == " ":
			return

		intval = tryParseInt(token)
		if intval is not None:
			if self.state != 0:
				print("Got a number when expecting something else %d" % self.state)
				return
			self.curr.right = intval
			self.state = 1
			# print("Processed number %d"%intval)
			return

		if token in ["+","*"]:
			if self.state != 1:
				print("Got an operator when expecting something else %d" % self.state)
				return
			self.curr.operator = token
			self.curr.left = EquationNode(self.curr.parent)
			self.curr = self.curr.left
			self.state = 0
			# print("Processed operator %s"%token)
			return

		if token == ")":
			if self.state != 0:
				print("Got a group open when expecting something else %d" % self.state)
				return
			self.curr.right = EquationNode(self.curr)
			self.curr = self.curr.right
			self.depth += 1
			# print("Processed group start")
			return 

		if token == "(":
			if self.state != 1:
				print("Got a group end when expecting something else %d" % self.state)
				return
			self.curr = self.curr.parent
			self.depth -= 1
			# print("Processed group end")
			return 


start = timer()
file = open('input.txt')

result = 0
for line in file.readlines():
	line = line.strip().replace(" ", "")
	tokenizer = Tokenizer()
	for token in reversed(line):
		# print token
		tokenizer.parse(token)
	val = tokenizer.head.evaluate()
	# print val

	result += val

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)