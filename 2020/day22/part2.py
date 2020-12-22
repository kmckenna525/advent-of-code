from timeit import default_timer as timer


def take_snapshot(decks):
	return ",".join(str(x) for x in decks[0]) + "|" + ",".join(str(x) for x in decks[1])

in_decks = []

start = timer()
file = open('input.txt')

in_deck = None
for line in file.readlines():
	line = line.strip()
	if line == "":
		continue

	if "Player" in line:
		in_deck = []
		in_decks.append(in_deck)
		continue

	in_deck.append(int(line))

def play(decks):
	states = set()
	while len(decks[0]) > 0 and len(decks[1]) > 0:
		snap = take_snapshot(decks)

		# don't loop 
		if snap in states:
			return (0, decks[0])

		states.add(snap)

		round_check = [decks[0].pop(0), decks[1].pop(0)]

		if len(decks[0]) >= round_check[0] and len(decks[1]) >= round_check[1]:
			(round_i, round_deck) = play([decks[0][:round_check[0]], decks[1][:round_check[1]]])
		elif round_check[0] > round_check[1]:
			round_i = 0
		else:
			round_i = 1

		decks[round_i].append(round_check[round_i])
		decks[round_i].append(round_check[round_i - 1])



	if len(decks[0]) > 0:
		return (0, decks[0])
	else:
		return (1, decks[1])

(index, winner) = play(in_decks)

result = 0
length = len(winner)
for i in range(0, length):
	multiplier = length - i
	result += winner[i] * multiplier


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)