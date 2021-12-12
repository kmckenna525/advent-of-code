from timeit import default_timer as timer
import re
import math

start = timer()
file = open('input.txt')

target = int(file.read().strip())


def isprime(number):
	sqrt = math.sqrt(number)
	for factor in range(2, int(sqrt)+1):
		if (number % factor) == 0:
			return False
	return True


def factorize(number):
	sqrt = int(math.sqrt(number))
	yield 1
	yield number
	for factor in range(2, sqrt+1):
		if (number % factor) == 0:
			yield factor
			yield int(number/factor)


def calculate(number):
	total = 0
	for i in factorize(number):
		total += i
	return total * 10


result = -1
for i in range(1,(target/10 - 1)):
	# print "House %d got %d presents." % (i, calculate(i))
	if calculate(i) >= target:
		result = i
		break

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)