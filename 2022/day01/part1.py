from timeit import default_timer as timer

start = timer()
file = open('input.txt')

elves = [0]
elfIndex = 0
result = 0
for line in file.readlines():
	line = line.strip()
	if len(line) == 0:
		if elves[elfIndex] > result:
			result = elves[elfIndex]

		elves.append(0)
		elfIndex += 1
		continue

	elves[elfIndex] += int(line)

if elves[elfIndex] > result:
	result = elves[elfIndex]

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)