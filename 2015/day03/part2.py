from timeit import default_timer as timer

directions = {
	"^": (0,1),
	"v": (0,-1),
	">": (1,0),
	"<": (-1,0)
}

def add(a, b):
	return (a[0] + b[0], a[1] + b[1])

start = timer()
file = open('input.txt')

seen = {(0,0)}
santa = (0,0)
robo = (0,0)
flip = False
result = 1
for move in file.readlines()[0]:
	direction = directions.get(move, (0,0))

	curr = direction
	if flip:
		robo = add(robo, direction)
		curr = robo
	else:
		santa = add(santa, direction)
		curr = santa

	flip = not flip
	if curr not in seen:
		result += 1
		seen.add(curr)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)