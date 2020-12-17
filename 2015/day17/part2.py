from timeit import default_timer as timer

target = 150

start = timer()
file = open('input.txt')

def permute(vals, target):
	if len(vals) <=1:
		if len(vals) == 1 and vals[0] == target:
			return [vals]
		return []
	else:
		ret = []
		vals = [] + vals
		while(len(vals) > 0):
			val = vals[0]
			vals.pop(0)
			if val > target:
				continue
			if val == target:
				ret.append([val])
				continue
			for perm in permute(vals, target - val):
				ret.append([val] + perm)
		return ret

containers = []
for line in file.readlines():
	containers.append(int(line.strip()))

containers.sort(reverse=True)

permutations = permute(containers, target)
smallest = len(containers)
matches = []
for perm in permutations:
	length = len(perm)
	if length < smallest:
		# print (length, perm)
		matches = [perm]
		smallest = length
	elif length == smallest:
		# print perm
		matches.append(perm)

result = len(matches)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)