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

		count += 1

		a = numbers[i]
		b = numbers[j]
		if a + b == 2020:
			print("%d iterations in %fms" % (count, (timer() - start) * 1000))
			print("\n%d * %d = %d" % (a,b,a*b))

print("\nworst case: %d iterations" % count)

# 1069 * 951 = 1016619