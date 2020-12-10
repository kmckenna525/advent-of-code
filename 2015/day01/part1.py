from timeit import default_timer as timer

file = open('input.txt')


line = file.readlines()[0]
floor = 0
start = timer()
for val in line:
	if val == "(":
		floor += 1
	if val == ")":
		floor -= 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("floor %d" % floor)
