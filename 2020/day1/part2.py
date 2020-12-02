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

		for k in range(2, length):
			if i == k or j == k:
				continue

			count += 1

			a = numbers[i]
			b = numbers[j]
			c = numbers[k]
			if a + b + c == 2020:
				print("%d * %d * %d = %d" % (a,b,c,a*b*c))
				print("%d iterations; O(%d^3) = %d" % (count, length, length * length * length))
				exit(0)
