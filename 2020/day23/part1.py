from timeit import default_timer as timer

ITERATIONS = 100
PICKUP = 3

class Node:
	def __init__(self, val):
		self.val = val
		self.next = None

	def __str__(self):
		return  str(self.val)

	def __repr__(self):
		return  str(self.val)

	def pop_next(self):
		if not self.next:
			return None #??? shouldn't happen
		prevnext = self.next
		self.next = self.next.next
		prevnext.next = None
		return prevnext

	def insert_after(self, new):
		prevnext = self.next
		self.next = new
		new.next = prevnext

def arr_has_val(arr, val):
	for other in arr:
		if other.val == val:
			return True
	return False

class Circle:
	def __init__(self, line):
		self.map = {}
		self.highest = 9 # known from input
		self.lowest = 1 # known from input
		self.first = int(line[0])

		head = None
		prev = None
		for num in line:
			num = int(num)
			if prev:
				prev.next = Node(num)
				prev = prev.next
			else:
				prev = Node(num)
			self.map[num] = prev
			if head is None:
				head = prev
		prev.next = head

	def __str__(self):
		ret = ""
		for val in self.iterate():
			ret += str(val)
		return ret

	def __repr__(self):
		return str(self)

	def insert(self, curr, vals):
		for val in reversed(vals):
			curr.insert_after(val)

	def pickup(self, curr):
		pickup = []
		while len(pickup) < PICKUP:
			pickup.append(curr.pop_next())
		return pickup

	def find(self, val):
		return self.map[val]

	def wrap(self, val):
		# assumes that we don't go lower than -1
		if val < self.lowest:
			return self.highest 
		if val > self.highest:
			return self.lowest
		return val 

	def target(self, basis, exclude):
		target = self.wrap(basis - 1)
		while arr_has_val(exclude, target):
			target = self.wrap(target - 1)
		return self.find(target)

	def iterate(self, start_label = 1):
		head = self.map[start_label]
		yield head.val
		curr = head.next
		while curr != head:
			yield curr.val
			curr = curr.next


start = timer()
file = open('input.txt')

cups = Circle(file.readlines()[0].strip())

curr = cups.find(cups.first)
for i in range(ITERATIONS):
	# print "Move %d"%(i+1)
	label = curr.val
	# print (label)
	pickup = cups.pickup(curr)
	destination = cups.target(label, pickup)
	# print pickup
	# print (destination)


	cups.insert(destination, pickup)
	curr = curr.next
	# print list(cups.iterate(label))
	# print


result = str(cups)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%s is the result" % result)






