from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

# exponential growth, every 7 days, after 0
# unsynchronized
# +2 day before first cycle

class LanternFish:
	def __init__(self, initial_clock, spawn_clock, cycle):
		self.clock = initial_clock
		self.spawn = spawn_clock
		self.cycle = cycle

	def __str__(self):
		return  "%d" % (self.clock)

	def __repr__(self):
		return  "%d" % (self.clock)

	# returns baby if clock is up
	def tick(self):
		self.clock -= 1
		if self.clock < 0:
			self.clock = self.cycle
			return LanternFish(self.spawn, self.spawn, self.cycle)


spawn = 8
cycle = 6
fishes = []
for initial_clock in file.readlines()[0].split(","):
	fishes.append(LanternFish(int(initial_clock), spawn, cycle))

days = 80
for day in range(0, days):
	bebes = []
	for fish in fishes:
		newb = fish.tick()
		if newb is not None:
			bebes.append(newb)
	fishes.extend(bebes)


result = len(fishes)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)