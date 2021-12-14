from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')


class Rule:
	def __init__(self, target, insert):
		self.target = target
		self.insert = insert
		self.left = None
		self.right = None

	def __str__(self):
		return  "%s -> %s" % (self.target, self.insert)

	def __repr__(self):
		return  "%s -> %s" % (self.target, self.insert)


def initialize_graph(rules):
	for rule in rules.copy().values():
		left = rule.target[0] + rule.insert
		rule.left = rules[left]
		right = rule.insert + rule.target[1] 
		rule.right = rules[right]



def add(to_update, key, val):
	if key not in to_update:
		to_update[key] = 0
	to_update[key] += val


def addmap(to_update, to_add):
	for key, val in to_add.items():
		add(to_update, key, val)


def initialize_counts(template, counter):
	for char in template:
		add(counter, char, 1)

memo = {}
def memoize(rule, remaining, counter):
	key = (rule.target, remaining)
	memo[key] = counter.copy()

def get_memo(rule, remaining):
	key = (rule.target, remaining)
	return memo[key] if key in memo else None


def count_nodes(rule, remaining):
	remaining -= 1

	memoval = get_memo(rule, remaining)
	if memoval is not None:
		return memoval
	
	counter = {}
	add(counter, rule.insert, 1)

	if remaining > 0:
		# recurse both sides
		addmap(counter, count_nodes(rule.left, remaining))
		addmap(counter, count_nodes(rule.right, remaining))

	memoize(rule, remaining, counter)
	return counter


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

	rules[target] = Rule(target, output)
	
	linecount += 1

initialize_graph(rules)
counts = {}
initialize_counts(template, counts)

steps = 40
for i in range(0, len(template) - 1):
	pair = template[i:i+2]
	if pair in rules:
		addmap(counts, count_nodes(rules[pair], steps))

least = float("inf")
most = 0
for key, val in counts.items():
	if val > most:
		most = val
	if val < least:
		least = val

result = most - least

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)