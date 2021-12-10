from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

scores = {
	")": 3,
	"]": 57,
	"}": 1197,
	">": 25137
}

pair = {
	"(": ")",
	"[": "]",
	"{": "}",
	"<": ">",
}

class Stack:
	def __init__(self):
		self.stack = []

	def __str__(self):
		return str(self.stack)

	def __repr__(self):
		return str(self.stack)

	@property
	def is_empty(self):
		return True if len(self.stack) == 0 else False

	@property
	def length(self):
		return len(self.stack)

	@property
	def top(self):
		return self.stack[-1]  

	def push(self, x):
		self.x = x
		self.stack.append(x)       

	def pop(self):
		return self.stack.pop()


def try_parse(line):
	stack = Stack()
	for char in line:
		if char in pair: # it's an opener
			stack.push(char)
			continue

		# otherwise it's a closer
		if stack.is_empty:
			# print("Expected opener, but found %s instead." % (char))
			return (None, char) # extra closer with no opener

		top = stack.top
		if char != pair[top]:
			# print("Expected %s, but found %s instead." % (pair[top], char))
			return (None, char) # wrong closer

		# valid case
		stack.pop()
	return (stack.length == 0, stack)



result = 0
for line in file.readlines():
	is_complete, info = try_parse(line.strip())
	if is_complete == None:
		result += scores[info]

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)