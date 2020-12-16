from timeit import default_timer as timer
import re

class Field:
	def __init__(self, info):
		self.name = info["name"]
		ranges = []
		ranges.append((int(info["min1"]),int(info["max1"])))
		ranges.append((int(info["min2"]),int(info["max2"])))
		self.ranges = ranges
		self.invalid = set()
		self.valid = set()

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

def parse_ticket(line):
	ticket = []
	for num in line.split(","):
		ticket.append(int(num))
	for val in ticket:
		if not any_valid(val):
			return
	tickets.append(ticket)

def first(iterable):
	for item in iterable:
		return item

my_ticket = []
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
		for num in line.split(","):
			my_ticket.append(int(num))
	else:
		if line == "nearby tickets:":
			continue
		parse_ticket(line)

length = len(tickets[0])
known = {}
while len(fields) > 0:
	field = fields[0]
	for ticket in tickets:
		for i in range(0, length):
			if i in field.invalid or i in known:
				continue

			if field.is_valid(ticket[i]):
				field.valid.add(i)
			else:
				if i in field.valid:
					field.valid.remove(i)
				field.invalid.add(i)
		if len(field.valid) == 1:
			break;
	fields.pop(0)
	if len(field.valid) == 1:
		known[first(field.valid)] = field
	elif len(field.valid) == 0:
		print ("uhhhhhhh error?", field)
	else:
		field.valid = set()
		fields.append(field)

result = 1
for (index, field) in known.items():
	if field.name[0:9] == "departure":
		result *= my_ticket[index]

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)