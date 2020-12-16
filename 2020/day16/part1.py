from timeit import default_timer as timer
import re

class Field:
	def __init__(self, info):
		self.name = info["name"]
		ranges = []
		ranges.append((int(info["min1"]),int(info["max1"])))
		ranges.append((int(info["min2"]),int(info["max2"])))
		self.ranges = ranges

	def __str__(self):
		return  "%s" % (self.name)

	def __repr__(self):
		return  "%s" % (self.name)

	def is_valid(self, val):
		for bucket in self.ranges:
			if val >= bucket[0] and val <= bucket[1]:
				return True
		return False

start = timer()
file = open('input.txt')

fieldpattern = r"(?P<name>.+): (?P<min1>\d+)-(?P<max1>\d+) or (?P<min2>\d+)-(?P<max2>\d+)";
fields = []
tickets = []

def any_valid(val):
	for field in fields:
		if field.is_valid(val):
			return True
	return False

state = 0
for line in file.readlines():
	line = line.strip()
	if len(line) == 0:
		state += 1
		continue

	if state == 0:
		matches = re.match(fieldpattern, line)
		data = matches.groupdict()
		fields.append(Field(data))

	elif state == 1:
		if line == "your ticket:":
			continue
		#noop for part 1
	else:
		if line == "nearby tickets:":
			continue
		ticket = []
		for num in line.split(","):
			ticket.append(int(num))
		tickets.append(ticket)

error_rate = 0
for ticket in tickets:
	for val in ticket:
		if not any_valid(val):
			error_rate += val

result = error_rate

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)