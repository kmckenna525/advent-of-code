from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

raw = 0
processed = 0
for line in file.readlines():
	line = line.strip()
	raw += len(line)

	# handle ""
	line = line[1:-1]

	#handle escapes
	line = line.replace("\\\\","\\")
	line = line.replace("\\\"","\"")

	#handle unicode
	line = re.sub(r"\\x[0-9a-fA-F]{2}",".", line)
	
	processed += len(line)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % (raw - processed))