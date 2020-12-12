from timeit import default_timer as timer

iterations = 50

def readline(line):
	result = ""
	prev = line[0]
	count = 1
	for i in range(1, len(line)):
		char = line[i]
		if char == prev:
			count += 1
		else:
			result += str(count) + prev
			count = 1
			prev = char
	result += str(count) + prev
	return result

start = timer()
file = open('input.txt')

line = file.readlines()[0].strip()

for i in range(0, iterations):
	line = readline(line)

result = len(line)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)