from timeit import default_timer as timer
import re

def test(program): 
	result = 0
	curr = 0
	seen = set()
	while curr not in seen:
		seen.add(curr)

		if curr >= len(program):
			return (True, result)

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

	return (False, result)

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
for i in range(0,len(program)):
	(cmd, arg) = program[i]
	if cmd == "nop": 
		program[i] = ("jmp", arg)
		(no_loop, result) = test(program)
		if no_loop:
			break
		program[i] = ("nop", arg)
	elif cmd == "jmp": 
		program[i] = ("nop", arg)
		(no_loop, result) = test(program)
		if no_loop:
			break
		program[i] = ("jmp", arg)


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)