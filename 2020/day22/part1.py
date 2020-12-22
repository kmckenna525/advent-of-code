from timeit import default_timer as timer

decks = []

start = timer()
file = open('input.txt')

in_deck = None
for line in file.readlines():
	line = line.strip()
	if line == "":
		continue

	if "Player" in line:
		in_deck = []
		decks.append(in_deck)
		continue

	in_deck.append(int(line))

while len(decks[0]) > 0 and len(decks[1]) > 0:
	a = decks[0].pop(0)
	b = decks[1].pop(0)

	if a > b:
		decks[0].append(a)
		decks[0].append(b)
	if b > a:
		decks[1].append(b)
		decks[1].append(a)

winner = decks[0]
if len(winner) == 0:
	winner = decks[1]

result = 0
length = len(winner)
for i in range(0, length):
	multiplier = length - i
	result += winner[i] * multiplier


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)