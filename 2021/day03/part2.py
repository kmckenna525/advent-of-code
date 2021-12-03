from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

lines = file.readlines()
bitcount = len(lines[0].strip())

def most_common_bit(sublist, i):
	count0 = 0
	count1 = 0
	for binarynum in sublist:
		if binarynum[i] == "0":
			count0 += 1
		if binarynum[i] == "1":
			count1 += 1
	if count0 == count1:
		return None
	if count1 > count0:
		return "1"
	else:
		return "0"

def filter_targets(sublist, bit, target):
	for i in reversed(range(0, len(sublist))):
		if sublist[i][bit] != target:
			sublist.pop(i)

numlist = []
for line in lines:
	binarynum = line.strip()
	numlist.append(binarynum)

oxygengens = [] + numlist
for i in range(0, bitcount):
	most_common = most_common_bit(oxygengens, i)
	target = most_common
	if most_common is None:
		target = "1"

	filter_targets(oxygengens, i, target)
	if len(oxygengens) == 1:
		break

co2scrubs = [] + numlist
for i in range(0, bitcount):
	most_common = most_common_bit(co2scrubs, i)
	target = most_common
	if most_common is None:
		target = "0"
	elif most_common == "0":
		target = "1"
	else: 
		target = "0"

	filter_targets(co2scrubs, i, target)
	if len(co2scrubs) == 1:
		break



oxygengen = int(oxygengens[0], 2)
co2scrub = int(co2scrubs[0], 2)
result = oxygengen * co2scrub

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d, %d: %d is the result" % (oxygengen, co2scrub, result))