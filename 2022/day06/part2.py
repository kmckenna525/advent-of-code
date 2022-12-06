from timeit import default_timer as timer

start = timer()
file = open('input.txt')

line = file.read().strip()
for i in range(0, len(line) - 14):
	uniq = set(line[i:i+14])
	if len(uniq) == 14:
		result = i + 14
		break


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)