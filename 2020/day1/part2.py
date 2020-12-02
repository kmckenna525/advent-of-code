from timeit import default_timer as timer

file = open('input.txt')

numbers = []
for line in file.readlines():
	numbers.append(int(line.strip()))

length = len(numbers)

count = 0
start = timer()
for i in range(length):
	for j in range(i + 1, length):
		if i == j:
			continue

		for k in range(j + 2, length):
			if i == k or j == k:
				continue

			count += 1

			a = numbers[i]
			b = numbers[j]
			c = numbers[k]
			if a + b + c == 2020:
				print("%d iterations in %fms" % (count, (timer() - start) * 1000))
				print("\n%d * %d * %d = %d" % (a,b,c,a*b*c))
			
print("\nworst case: %d iterations" % count)


# 473 * 405 * 1142 = 218767230