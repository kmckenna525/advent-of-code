from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

vowels = r"([aeiou].*?){3}"
double = r"(.)\1"
restricted = r"ab|cd|pq|xy"

result = 0
for line in file.readlines():
	trimmed = line.strip()
	if not re.search(vowels, trimmed):
		# print("not enough vowels", trimmed)
		continue
	if not re.search(double, trimmed):
		# print("no doubles found", trimmed)
		continue
	if re.search(restricted, trimmed):
		# match = re.search(restricted, trimmed)
		# print("restricted sequence", trimmed[match.start(0):match.end(0)], trimmed)
		continue
	
	result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)