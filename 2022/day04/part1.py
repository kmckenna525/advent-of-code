from timeit import default_timer as timer

start = timer()
file = open('input.txt')

def fully_contains(outer, inner):
	return inner[0] >= outer[0] and inner[1] <= outer[1]

result = 0
for line in file.readlines():
	line = line.strip()
	ranges = line.split(',')
	elf1 = [int(x) for x in ranges[0].split('-')]
	elf2 = [int(x) for x in ranges[1].split('-')]

	if fully_contains(elf1, elf2) or fully_contains(elf2, elf1):
		result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)