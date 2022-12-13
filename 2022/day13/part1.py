from timeit import default_timer as timer
import json

start = timer()
file = open('input.txt')

def convert(val):
	return [val]

def compare(left, right):
	# print left, "vs", right
	if isinstance(left, int) and isinstance(right, int):
		if left < right:
			return -1
		elif left == right:
			return 0
		else:
			return 1

	if isinstance(left, int):
		left = convert(left)

	if isinstance(right, int):
		right = convert(right)

	lenleft = len(left)
	lenright = len(right)

	i = 0
	while True:
		# exit cases are hitting the end of the lists
		if i >= lenleft:
			if lenleft == lenright:
				return 0
			return -1

		if i >= lenright:
			return 1

		# now recurse into them
		comp = compare(left[i], right[i])
		if comp != 0:
			return comp

		i += 1


result = 0
index = 1
for in_pair in file.read().split("\n\n"):
	[left, right] = [json.loads(packet) for packet in in_pair.split("\n")]
	
	if compare(left, right) == -1:
		# print index
		result += index

	index += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)