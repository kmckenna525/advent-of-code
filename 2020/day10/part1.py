from timeit import default_timer as timer

start = timer()
file = open('input.txt')

# pre process input
values = []
for line in file.readlines():
	values.append(int(line))
values.sort()

# add highest +3 for the built in
values.append(values[-1] + 3)

diffs = {
	0: 0,
	1: 0,
	2: 0,
	3: 0
}
prev = 0
for val in values:
	diffs[val - prev] += 1
	prev = val

result = diffs[1] * diffs[3]

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)