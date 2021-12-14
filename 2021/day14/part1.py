from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

template = None
rules = {}
pattern = r"(?P<target>\w+) -> (?P<output>\w+)";
linecount = 0
for line in file.readlines():
	linecount += 1
	if linecount == 1:
		template = line.strip()
		continue
	if linecount == 2:
		continue

	matches = re.match(pattern, line)
	data = matches.groupdict();
	target = data["target"]
	output = data["output"]

	rules[target] = output
	
	linecount += 1

def apply(template, rules):
	newval = ""
	insertcount = 0
	for i in range(0, len(template) - 1):
		pair = template[i:i+2]
		newval += pair[0]
		if pair in rules:
			newval += rules[pair]
	newval += template[-1]
	return newval

steps = 10
polymer = template
for i in range(0,steps):
	polymer = apply(polymer, rules)

counts = {}
for char in polymer:
	if char not in counts:
		counts[char] = 0
	counts[char] += 1

least = len(polymer)
most = 0
for key, val in counts.items():
	if val > most:
		most = val
	if val < least:
		least = val

result = most - least

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)