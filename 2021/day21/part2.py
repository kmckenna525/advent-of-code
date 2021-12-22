from timeit import default_timer as timer
from collections import namedtuple
import itertools
import re

start = timer()
file = open('input.txt')

spaces = 10
diesides = 3
rolls = 3
target_score = 21


Player = namedtuple('Player', ['id', 'space', 'score'])


def add_wins(wins, other):
	return (wins[0] + other[0], wins[1] + other[1])


def move_player(player, amount):
	space = (player.space + amount) % spaces
	return Player(player.id, space, player.score + space + 1)


def next_player(playernum):
	return (playernum + 1) % 2


def get_player(player1, player2, playerturn):
	if playerturn == 0:
		return player1
	return player2


memo = {} #state to wins
def get_winsr(player1, player2, playerturn = 0):
	# print depth, player1.score, player2.score, rolltotal, rollcount,  playerturn
	key = (player1, player2, playerturn)
	if key in memo:
		return memo[key]

	wins = (0,0)
	for rolls in itertools.product([1, 2, 3], repeat=3):
		rolltotal = sum(rolls)
		players = [player1, player2]
		players[playerturn] = move_player(players[playerturn], rolltotal)
		# print players[playerturn].score
		if players[playerturn].score >= target_score:
			nextwins = (1 if playerturn == 0 else 0, 1 if playerturn == 1 else 0)
			wins = add_wins(wins, nextwins)
			# print "win"
		else:
			nextwins = get_winsr(players[0], players[1], next_player(playerturn))
			wins = add_wins(wins, nextwins)

	memo[key] = wins
	return wins


def get_wins(player1, player2, rolltotal, rollcount, playerturn):
	states = [(player1, player2, rolltotal, rollcount, playerturn)]
	wins = [0,0]
	while len(states) > 0:
		player1, player2, rolltotal, rollcount, playerturn = states.pop()
		# print wins, player1.score, player2.score, rolltotal, rollcount, playerturn
		if rollcount >= rolls:
			player = None
			if playerturn == 0:
				player1 = move_player(player1, rolltotal)
				player = player1
			else:
				player2 = move_player(player1, rolltotal)
				player = player2
			if player.score >= target_score:
				wins[playerturn] += 1
				print wins[playerturn]
				continue

			rolltotal = 0
			rollcount = 0
			playerturn = next_player(playerturn)

		for roll in range(1, diesides + 1):
			states.append((player1, player2, rolltotal + roll, rollcount + 1, playerturn))

	return wins




pattern = r"Player (?P<playerid>\d+) starting position: (?P<space>\d+)";
result = 0
players = []
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	playerid = int(data["playerid"])
	space = int(data["space"])

	players.append(Player(playerid, space - 1, 0))


wins = get_winsr(players[0], players[1])
result = max(wins)

print("Completed in %fms" % ((timer() - start) * 1000))
print wins
print("%d is the result" % result)











