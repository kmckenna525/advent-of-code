from timeit import default_timer as timer

start = timer()
file = open('input.txt')

def overlaps(outer, inner):
	return inner[1] >= outer[0] and inner[0] <= outer[1]

result = 0
for line in file.readlines():
	line = line.strip()
	ranges = line.split(',')
	elf1 = [int(x) for x in ranges[0].split('-')]
	elf2 = [int(x) for x in ranges[1].split('-')]

	if overlaps(elf1, elf2):
		result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)