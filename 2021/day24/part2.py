from timeit import default_timer as timer
from collections import namedtuple
import re

start = timer()
file = open('input.txt')

Instruction = namedtuple('Instruction', ['op', 'a', 'b'])

def process(variables, instr, iterinput):
	op, a, b = instr
	if b is not None and not isinstance(b, int):
		b = variables[b]
	if instr.op == "inp":
		variables[a] = int(next(iterinput))
	elif instr.op == "add":
		variables[a] += b
	elif instr.op == "mul":
		variables[a] *= b
	elif instr.op == "div":
		variables[a] /= b
	elif instr.op == "mod":
		variables[a] %= b
	elif instr.op == "eql":
		variables[a] = 1 if variables[a] == b else 0


def run(monad, inputs):
	iterinput = iter(inputs)
	variables = {"w": 0, "x": 0, "y": 0, "z": 0}
	for instr in monad:
		process(variables, instr, iterinput)
	print variables
	return variables["z"]


monad = []

pattern = r"(?P<op>inp|add|mul|div|mod|eql) (?P<a>\w+)( (?P<b>(-|\w)+))?"
for line in file.readlines():
	if len(line.strip()) == 0 or line[0] == "#":
		continue
	matches = re.match(pattern, line.split("#")[0].strip())
	data = matches.groupdict();
	op = data["op"]
	a = data["a"]
	b = data["b"]

	if b is not None and b.strip("-").isdigit():
		b = int(b)

	monad.append(Instruction(op,a,b))

inputs = 13161151139617
print run(monad, str(inputs))
# inputs = int("1" * 14)
# while run(monad, str(inputs)) != 0:
# 	print inputs
# 	inputs -= 1

result = inputs
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)