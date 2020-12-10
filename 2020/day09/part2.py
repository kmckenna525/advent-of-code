from timeit import default_timer as timer

target = 10884537

start = timer()
file = open('input.txt')

numbers = []

for line in file.readlines():
	num = int(line)
	numbers.append(num)

length = len(numbers)
result = None
for first in range(0, length):
	total = 0
	smallest = None
	largest = None
	for i in range(first,length):
		num = numbers[i]
		total += num
		if(total > target):
			break

		if not smallest or smallest > num:
			smallest = num
		if not largest or largest < num:
			largest = num

		if total == target:
			result = smallest + largest
			break;

	if result:
		break


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)