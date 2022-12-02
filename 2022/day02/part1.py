from timeit import default_timer as timer

start = timer()
file = open('input.txt')

scores = {
	'A': 1,
	'B': 2,
	'C': 3,
	'X': 1,
	'Y': 2,
	'Z': 3
}

result = 0
for line in file.readlines():
	line = line.strip()
	[oppMove, move] = line.split()

	myNum = scores[move]
	oppNum = scores[oppMove]
	roundResult = myNum
	if oppNum == myNum:
		roundResult += 3
	elif myNum == 1 and oppNum == 3:
		roundResult += 6
	elif myNum == 2 and oppNum == 1:
		roundResult += 6
	elif myNum == 3 and oppNum == 2:
		roundResult += 6
	result += roundResult

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)