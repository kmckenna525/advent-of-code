from timeit import default_timer as timer

start = timer()
file = open('input.txt')

interesting = [20,60,100,140,180,220]

x = 1
cycle = 0
result = 0
for line in file.readlines():
	op_cycles = 1
	addx = 0
	if line[0] == "a":
		addx = int(line.split()[1])
		op_cycles = 2

	for i in range(op_cycles):
		cycle += 1
		if cycle in interesting:
			result += x * cycle
	x += addx
	
file.close()


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)