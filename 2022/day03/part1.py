from timeit import default_timer as timer

start = timer()
file = open('input.txt')

def num_for_item(item):
	num = ord(item)
	if num >= 97: # lowercase
		return num - 96
	return num - 38 # - 64 + 26

result = 0
for line in file.readlines():
	line = line.strip()
	mid = len(line)/2
	first = line[:mid]
	second = line[mid:]

	for item in first:
		if item in second:
			result += num_for_item(item)
			break

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)