from timeit import default_timer as timer

start = timer()
file = open('input.txt')

is_fresh = True
group = set()
result = 0
for line in file.readlines():
	if(line == "\n"):
		result += len(group)
		group.clear()
		is_fresh = True
		continue

	if len(group) == 0:
		if is_fresh:
			is_fresh = False
			for answer in line:
				if(answer != "\n"):
					group.add(answer)
		continue

	group = group.intersection(line)

result += len(group)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)