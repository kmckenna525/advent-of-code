from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

pattern = r"(?P<cmd>\w+) (?P<sign>[+-])(?P<arg>\d+)";
program = []
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	cmd = data["cmd"]
	sign = data["sign"]
	arg = int(data["arg"])

	if sign == "-":
		arg = -arg

	program.append((cmd, arg))

result = 0
curr = 0
seen = set()
while curr not in seen:
	seen.add(curr)
	(cmd, arg) = program[curr]

	if cmd == "nop": 
		curr += 1
		continue

	if cmd == "acc": 
		result += arg
		curr += 1
		continue

	if cmd == "jmp": 
		curr += arg
		continue

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)