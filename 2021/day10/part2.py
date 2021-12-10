from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

scores = {
	")": 1,
	"]": 2,
	"}": 3,
	">": 4
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


def finish_line(stack):
	ending = ""
	while not stack.is_empty:
		ending += pair[stack.pop()]
	return ending
	

def score_line(ending):
	total = 0
	for char in ending:
		total *= 5
		total += scores[char]
	return total


line_scores = []
for line in file.readlines():
	is_complete, info = try_parse(line.strip())
	if is_complete == False:
		line_scores.append(score_line(finish_line(info)))

line_scores = list(sorted(line_scores))
result = line_scores[len(line_scores) / 2]
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)