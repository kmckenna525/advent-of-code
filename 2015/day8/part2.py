from timeit import default_timer as timer

start = timer()
file = open('input.txt')

raw = 0
processed = 0
for line in file.readlines():
	line = line.strip()
	raw += len(line)

	#handle escapes
	line = line.replace("\\","\\\\")
	line = line.replace("\"","\\\"")

	# handle ""
	line = "\"%s\"" % line
	
	processed += len(line)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % (processed - raw))