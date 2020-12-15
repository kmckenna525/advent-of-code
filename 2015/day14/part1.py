from timeit import default_timer as timer
import re

target = 2503

class Reindeer:
	def __init__(self, info):
		self.name = info["name"]
		self.speed = int(info["speed"])
		self.max = int(info["max"])
		self.rest = int(info["rest"])

	def __str__(self):
		return  "%s" % (self.name)

	def __repr__(self):
		return  "%s" % (self.name)

	def race(self, time):
		interval = self.max + self.rest
		cycles = int(time/interval)
		distance = self.speed * self.max * cycles
		remainder = time % interval
		if remainder > 0:
			distance += self.speed * min(self.max, remainder)
		return distance


start = timer()
file = open('input.txt')

pattern = r"(?P<name>\w+) can fly (?P<speed>\d+) km/s for (?P<max>\d+) seconds, but then must rest for (?P<rest>\d+) seconds.";

winning = 0
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	reindeer = Reindeer(data)

	distance = reindeer.race(target)
	# print (reindeer, distance)
	if distance > winning:
		winning = distance

result = winning
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)