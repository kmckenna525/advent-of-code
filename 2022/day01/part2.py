from timeit import default_timer as timer

start = timer()
file = open('input.txt')

elves = [0]
elfIndex = 0
for line in file.readlines():
	line = line.strip()
	if len(line) == 0:
		elves.append(0)
		elfIndex += 1
		continue

	elves[elfIndex] += int(line)
	
elves.sort()
result = elves[-1] + elves[-2] + elves[-3]

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)