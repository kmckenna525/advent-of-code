from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

count = 3

class Window:
	def __init__(self, count):
		self.window = []
		self.count = count

	def __str__(self):
		return  "%d" % (self.window)

	def __repr__(self):
		return str(self.window)

	def enqueue(self, val):
		self.window.append(val)


	def dequeue(self):
		if len(self.window) < self.count:
			return
		self.window.pop(0)

	def sum(self):
		if len(self.window) < self.count:
			print len(self.window)
			return None
		total = 0
		for val in self.window:
			total += val
		return total




count = 3
windowPrev = Window(count)
windowNext = Window(count)
result = 0
for line in file.readlines():
	num = int(line.strip())

	windowNext.dequeue()
	windowNext.enqueue(num)

	sumNext = windowNext.sum()
	sumPrev = windowPrev.sum()
	if sumPrev is None or sumNext is None:
		#initing, do nothing
	elif sumNext > sumPrev:
		result += 1
		print "increased"

	windowPrev.dequeue()
	windowPrev.enqueue(num)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)