from timeit import default_timer as timer

start = timer()
file = open('input.txt')

interesting = [20,60,100,140,180,220]

register = 1
cycle = 0
result = 0
width = 40
height = 6
screen = []
for i in range(height):
	screen.append([0] * width)
x = 0
y = 0
for line in file.readlines():
	op_cycles = 1
	addx = 0
	if line[0] == "a":
		addx = int(line.split()[1])
		op_cycles = 2

	for i in range(op_cycles):
		# print x, register
		if abs(x - register) <= 1:
			screen[y][x] = 1
		# print "".join("#" if val == 1 else "." for val in screen[y])


		cycle += 1
		x += 1
		if x >= width:
			x = 0
			y += 1
	register += addx
	
file.close()

for row in screen:
	print "".join("#" if val == 1 else "." for val in row)


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)