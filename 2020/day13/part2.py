from timeit import default_timer as timer

class Equivalence:
	def __init__(self, target, mod):
		self.target = target
		self.mod = mod 

	def __str__(self):
		return  "t = %d (mod %d)" % (self.target, self.mod)

	def __repr__(self):
		return  "t = %d (mod %d)" % (self.target, self.mod)

	def passes(self, val):
		return (val % self.mod) == self.target

	def solve(self, val):
		for i in range(1, self.mod + 1):
			test = val * i
			if self.passes(test):
				return test
		print "howd we get here"
		return -1 # I don't think it is mathematically possible to reach this

start = timer()
file = open('input.txt')

buses = []
for bus in file.readlines()[1].strip().split(","):
	buses.append(int(bus) if bus != "x" else -1)

eqs = []
base_lcm = 1
for i in range(0, len(buses)):
	bus = buses[i]
	if bus == -1:
		continue
	target = (buses[i] - i) % bus
	eqs.append(Equivalence(target, bus))
	base_lcm *= bus

total = 0
for eq in eqs:
	lcm = base_lcm / eq.mod
	solution = eq.solve(lcm)
	# print eq
	# print("%d solution %d" %(lcm, solution))
	total += solution


result = total % base_lcm
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)