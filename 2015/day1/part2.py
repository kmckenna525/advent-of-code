from timeit import default_timer as timer

file = open('input.txt')


line = file.readlines()[0]
floor = 0
pos = 0
start = timer()
for val in line:
	pos += 1

	if val == "(":
		floor += 1
	if val == ")":
		floor -= 1

	if floor == -1:
		break

print("Completed in %fms" % ((timer() - start) * 1000))
print("first basement entry %d" % pos)
