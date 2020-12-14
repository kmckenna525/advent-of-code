from timeit import default_timer as timer
import re
import itertools

class FloatMask:
	def __init__(self, target_index):
		self.target_index = target_index
		andmask = ["1"] * 36
		ormask = ["0"] * 36
		andmask[target_index] = "0"
		ormask[target_index] = "1"
		self.andmask = int("".join(andmask), 2)
		self.ormask = int("".join(ormask), 2)
  
	def __str__(self):
		return  "%d" % (self.val)

	def __repr__(self):
		return  "%d" % (self.val)

	def filter(self, vals):
		new = set()
		for val in vals:
			new.add(val & self.andmask)
			new.add(val | self.ormask)
		return vals.union(new)


class Mask:
	def __init__(self, val):
		self.val = val
		self.floats = []
		mask = ["0"] * 36
		for i in range(0, len(val)):
			if val[i] == "1":
				mask[i] = "1"
			if val[i] == "X":
				self.floats.append(FloatMask(i))
		self.mask = int("".join(mask), 2)
  
	def __str__(self):
		return  "%d" % (self.val)

	def __repr__(self):
		return  "%d" % (self.val)

	def filter(self, val):
		val = val | self.mask
		vals = set([val])
		for floating in self.floats:
			vals = floating.filter(vals)
		return vals


start = timer()
file = open('input.txt')

pattern = r"(mask = (?P<mask>\w+))|(mem\[(?P<addr>\d+)\] = (?P<value>\d+))";
current_mask = None
mem = {}
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	mask = data["mask"]
	addr = data["addr"]
	value = data["value"]

	if mask:
		current_mask = Mask(mask)
		continue

	if addr is not None:
		intval = int(value)
		addrs = current_mask.filter(int(addr))
		# print addrs
		for filtered in addrs:
			mem[filtered] = intval
	
result = 0
for addr,val in mem.items():
	result += val

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)