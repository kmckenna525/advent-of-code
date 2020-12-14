from timeit import default_timer as timer
import re

class Mask:
	def __init__(self, val):
		self.val = val
		andmask = ["1"] * 36
		ormask = ["0"] * 36
		for i in range(0, len(val)):
			if val[i] == "1":
				ormask[i] = "1"
			if val[i] == "0":
				andmask[i] = "0"
		self.andmask = int("".join(andmask), 2)
		self.ormask = int("".join(ormask), 2)
  
	def __str__(self):
		return  "%d" % (self.val)

	def __repr__(self):
		return  "%d" % (self.val)

	def filter(self, val):
		val = val & self.andmask
		val = val | self.ormask
		return val

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
		mem[int(addr)] = current_mask.filter(int(value))
	
result = 0
for addr,val in mem.items():
	result += val

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)