from timeit import default_timer as timer

start = timer()
file = open('input.txt')

scores = {
	'A': 1,
	'B': 2,
	'C': 3,
}

losses = {
	1: 3,
	2: 1,
	3: 2,
}

wins = {
	1: 2,
	2: 3,
	3: 1,
}

roundScores = {
	'X': 0,
	'Y': 3,
	'Z': 6,
}

result = 0
for line in file.readlines():
	line = line.strip()
	[oppMove, myRound] = line.split()

	roundScore = roundScores[myRound]
	oppNum = scores[oppMove]
	roundResult = roundScore

	if roundScore == 0:
		roundResult += losses[oppNum]
	elif roundScore == 3:
		roundResult += oppNum
	else:
		roundResult += wins[oppNum]

	result += roundResult

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)