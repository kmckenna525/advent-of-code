from timeit import default_timer as timer
import re

class Stack:
	def __init__(self):
		self.arr = []

	def is_empty(self):
		return len(self.arr) == 0

	def pop(self):
		return self.arr.pop()

	def top(self):
		return self.arr[-1]

	def push(self, val):
		return self.arr.append(val)


def try_parse_int(token):
	try:
		return int(token)
	except:
		return None

precedence = ["+","*"]
def parse(line):
	operators = Stack()
	operands = Stack()

	def process():
		# this is how you do the thing
		op = operators.pop()
		b = operands.pop()
		a = operands.pop()
		val = None
		if op == "+":
			val = a + b
		if op == "*":
			val = a * b
		operands.push(val)

	def next_op_is_gte(token):
		# if token is *, then every non-parend is equal or greater precedence
		# if token is +, then only + is equal or greater
		if token == "*" and operators.top() in precedence:
			return True
		if token == "+" and operators.top() == "+":
			return True
		return False

	for token in line:
		# print token
		intval = try_parse_int(token)
		if intval is not None:
			operands.push(intval)
		elif token == "(":
			operators.push(token)
		elif token == ")":
			while operators.top() != "(":
				process()
			operators.pop() # done with that group
		elif token in precedence:
			while not operators.is_empty() and next_op_is_gte(token):
				process()
			operators.push(token)

	while not operators.is_empty():
		process()

	# print operands.top()
	return operands.top()
			


start = timer()
file = open('input.txt')

result = 0
for line in file.readlines():
	result += parse(line.strip().replace(" ",""))

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)