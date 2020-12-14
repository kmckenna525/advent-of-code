from timeit import default_timer as timer
import json

def process(obj):
	if isinstance(obj, list):
		total = 0
		for item in obj:
			total += process(item)
		return total
	if isinstance(obj, dict):
		total = 0
		for key,item in obj.items():
			if item == "red" or key == "red":
				return 0
			total += process(item)
			total += process(key)
		return total
	if isinstance(obj, int):
		return obj

	return 0


start = timer()
file = open('input.txt')

result = 0
for line in file.readlines():
	obj = json.loads(line.strip())
	result += process(obj)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)