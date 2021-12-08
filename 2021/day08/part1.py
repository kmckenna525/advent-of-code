from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

# 7 segment display
#
# ideally
#  aaa
# b   c
# b   c
#  ddd
# e   f
# e   f
#  ggg
#
# 0 = abcefg  (6)
# 1 = cf      (2) *
# 2 = acdeg   (5)
# 3 = acdfg   (5)
# 4 = bcdf    (4) *
# 5 = abdfg   (5)
# 6 = abdefg  (6)
# 7 = acf     (3) *
# 8 = abcdefg (7) *
# 9 = abcdfg  (6)


def get_easy_number(signal):
	count = len(signal)
	if(count == 2):
		return 1
	if(count == 3):
		return 7
	if(count == 4):
		return 4
	if(count == 7):
		return 8
	return None

result = 0
for line in file.readlines():
	parts = line.strip().split(" | ")
	numbers = parts[0].split(" ")
	output = parts[1].split(" ")
	for signal in output:
		if get_easy_number(signal) is not None:
			result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)