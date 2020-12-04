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
curr = (0,0)
result = 1
for move in file.readlines()[0]:
	direction = directions.get(move, (0,0))
	curr = add(curr, direction)
	if curr not in seen:
		result += 1
		seen.add(curr)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)