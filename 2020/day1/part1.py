file = open('input.txt')

numbers = []
for line in file.readlines():
	numbers.append(int(line.strip()))

length = len(numbers)

count = 0
for i in range(length):
	for j in range(1, length):
		if i == j:
			continue

		count += 1

		a = numbers[i]
		b = numbers[j]
		if a + b == 2020:
			print("%d * %d = %d" % (a,b,a*b))
			print("%d iterations; O(%d^2) = %d" % (count, length, length * length))
			exit(0)
