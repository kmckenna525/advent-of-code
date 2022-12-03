from timeit import default_timer as timer

start = timer()
file = open('input.txt')

def num_for_item(item):
	num = ord(item)
	if num >= 97: # lowercase
		return num - 96
	return num - 38 # - 64 + 26

result = 0
group = []
for line in file.readlines():
	group.append(line.strip())

	if len(group) >= 3:
		for item in group[0]:
			if item in group[1] and item in group[2]:
				result += num_for_item(item)
				break
		group = []

	

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)