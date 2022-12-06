from timeit import default_timer as timer

start = timer()
file = open('input.txt')

line = file.read().strip()
for i in range(0, len(line) - 4):
	uniq = set(line[i:i+4])
	if len(uniq) == 4:
		result = i + 4
		break


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)