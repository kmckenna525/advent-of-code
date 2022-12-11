from timeit import default_timer as timer

start = timer()

def add(a, b):
	return a + b

def multiply(a, b):
	return a * b


class Item:
	def __init__(self, val):
		self.val = val

	def __str__(self):
		return  "%d" % (self.val)

	def __repr__(self):
		return str(self)


class Operation:
	def __init__(self, func, modifier):
		if func == "+":
			self.func = add
		else:
			self.func = multiply
		self.modifier = modifier if modifier == "old" else int(modifier)

	def __str__(self):
		return  "%s: %s" % (str(self.func), str(self.modifier))

	def __repr__(self):
		return str(self)

	def perform(self, val):
		if self.modifier == "old":
			return self.func(val, val)

		return self.func(val, self.modifier)


class Test:
	def __init__(self, mod_val, true_target, false_target):
		self.mod_val = int(mod_val)
		self.true_target = int(true_target)
		self.false_target = int(false_target)

	def __str__(self):
		return  "if |%d: %d; else %d" % (self.mod_val, self.true_target, self.false_target)

	def __repr__(self):
		return str(self)

	def perform(self, item):
		if item.val % self.mod_val == 0:
			return self.true_target
		return self.false_target


class Monkey:
	def __init__(self, name, starting, op, test):
		self.name = int(name)
		self.items = []
		for val in starting:
			self.items.append(Item(int(val.strip(","))))
		self.op = op
		self.test = test
		self.inspections = 0

	def __str__(self):
		return  "%d: %s" % (self.name, str(self.items))

	def __repr__(self):
		return str(self)

	def take_turn(self, others, worry_limit):
		while(len(self.items) > 0):
			item = self.items.pop(0)
			self.inspect(item, worry_limit)
			self.throw(item, others)


	def inspect(self, item, worry_limit):
		item.val = self.op.perform(item.val)
		item.val %= worry_limit
		self.inspections += 1


	def throw(self, item, others):
		target = others[self.test.perform(item)]
		# print(item, "throw to", target)
		target.items.append(item)

def perform_round(monkeys, worry_limit):
	for monkey in monkeys:
		monkey.take_turn(monkeys, worry_limit)

monkeys = []
worry_limit = 1
file = open('input.txt')
for monkey_in in file.read().split("\n\n"):
	lines = [i.split() for i in monkey_in.split("\n")]
	op = Operation(lines[2][4], lines[2][5])
	test = Test(lines[3][3], lines[4][5], lines[5][5])
	worry_limit *= test.mod_val
	monkeys.append(Monkey(lines[0][1][0], lines[1][2:], op, test))
file.close()

for i in range(10000):
	perform_round(monkeys, worry_limit)

monkey_business = []
for monkey in monkeys:
	monkey_business.append(monkey.inspections)
	
monkey_business.sort()
result = monkey_business[-1] * monkey_business[-2]

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)