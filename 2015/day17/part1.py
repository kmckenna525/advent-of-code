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

# matches = []
# for perm in permute(containers, target):
# 	print perm
# 	total = 0
# 	for container in perm:
# 		total += container
# 	if target == total:
# 		print perm
# 		matches.append(perm)

result = len(permute(containers, target))
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)