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
divider2 = [[2]]
divider6 = [[6]]
packets = [divider2, divider6]
for in_pair in file.read().split("\n\n"):
	packets += [json.loads(packet) for packet in in_pair.split("\n")]

packets = sorted(packets, cmp=compare)
result = (packets.index(divider2)+1) * (packets.index(divider6)+1)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)