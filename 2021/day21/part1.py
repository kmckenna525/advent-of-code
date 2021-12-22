from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

spaces = 10
rolls = 3
target_score = 1000


class DeterministicDie:
	def __init__(self, maxval):
		self.curr = 0
		self.max = maxval
		self.numrolls = 0

	def __str__(self):
		return  "%d" % (self.curr)

	def __repr__(self):
		return str(self.curr)

	def roll(self):
		val = self.curr
		self.curr = (self.curr + 1) % self.max
		self.numrolls += 1
		return val + 1


class Player:
	def __init__(self, playerid, space):
		self.id = playerid
		self.space = space
		self.score = 0

	def __str__(self):
		return  "%d" % (self.id)

	def __repr__(self):
		return str(self.id)


	def move(self, amount):
		self.space = (self.space + amount) % spaces
		self.score += self.space + 1 # base 1 instead of 0


def play(player, die):
	total = 0
	for i in range(0,rolls):
		total += die.roll()
	player.move(total)
	return player.score >= target_score


def other_player(player, players):
	if player.id == 1:
		return players[2]
	return players[1]


pattern = r"Player (?P<playerid>\d+) starting position: (?P<space>\d+)";
result = 0
players = {}
die = DeterministicDie(100)
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	playerid = int(data["playerid"])
	space = int(data["space"])

	players[playerid] = Player(playerid, space - 1)


winner = None
loser = None
while winner is None:
	didwin = False
	for player in players.values():
		if play(player, die):
			winner = player
			loser = other_player(player, players)
			break

result = die.numrolls * loser.score

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)













