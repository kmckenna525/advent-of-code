from timeit import default_timer as timer

target = 30000000

start = timer()
file = open('input.txt')

seen = {}
starting = file.readlines()[0].strip().split(",")
last_val = None
for i in range(0, len(starting)):
	val = int(starting[i])
	# print(val, i)
	if last_val or last_val == 0:
		seen[last_val] = i - 1
	last_val = val

for i in range(len(starting), target):
	if last_val in seen:
		val = i - seen[last_val] - 1
	else:
		val = 0
	seen[last_val] = i - 1
	last_val = val
	# print(val, i)


result = last_val

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)