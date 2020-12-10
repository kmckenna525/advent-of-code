from timeit import default_timer as timer

start = timer()
file = open('input.txt')

group = set()
result = 0
for line in file.readlines():
	if(line == "\n"):
		result += len(group)
		group.clear()
		continue

	for answer in line:
		if(answer != "\n"):
			group.add(answer)

result += len(group)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)