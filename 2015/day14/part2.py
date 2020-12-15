from timeit import default_timer as timer
import re

target = 2503

class Reindeer:
	def __init__(self, info):
		self.name = info["name"]
		self.speed = int(info["speed"])
		self.max = int(info["max"])
		self.rest = int(info["rest"])
		self.points = 0

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
reindeers = []
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	reindeer = Reindeer(data)
	reindeers.append(reindeer)

for time in range(1, target + 1):
	winning = (0, None)
	for reindeer in reindeers:
		distance = reindeer.race(time)
		# print (reindeer, distance)
		if distance > winning[0]:
			winning = (distance, [reindeer])
		elif distance == winning[0]:
			winning[1].append(reindeer)
	for winner in winning[1]:
		winner.points += 1

most_points = 0
for reindeer in reindeers:
	# print (reindeer, reindeer.points)
	if reindeer.points > most_points:
		most_points = reindeer.points

result = most_points
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)