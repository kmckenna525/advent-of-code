from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

pattern = r"((?P<val>\d+)|(?P<transfer>\w+)|(?P<in1>\w+) (?P<cmd>\w+) (?P<in2>\w+)|NOT (?P<not>\w+)) -> (?P<wire>\w+)";
wires = {}
delayed_wires = {}

def delay(delayed_wire, data):
	if delayed_wire not in delayed_wires:
		delayed_wires[delayed_wire] = []
	delayed_wires[delayed_wire].append(data)
	return False

def process_data(data):
	wire = data["wire"]
	val = int(data["val"]) if data["val"] else None
	transfer = data["transfer"]
	cmd = data["cmd"]
	in1 = data["in1"]
	in2 = data["in2"]
	not_in = data["not"]

	if val or val == 0:
		wires[wire] = val
	elif transfer:
		if transfer not in wires:
			return delay(transfer, data)
		wires[wire] = wires[transfer]
	elif not_in:
		if not_in.isdigit():
			not_in = int(not_in)
		else:
			if not_in not in wires:
				return delay(not_in, data)
			not_in = wires[not_in]
		wires[wire] = ~not_in & 0b1111111111111111
	elif cmd:
		if in1.isdigit():
			in1 = int(in1)
		else:
			if in1 not in wires:
				return delay(in1, data)
			in1 = wires[in1]
		if in2.isdigit():
			in2 = int(in2)
		else:
			if in2 not in wires:
				return delay(in2, data)
			in2 = wires[in2]

		if cmd == "AND":
			wires[wire] = in1 & in2
		elif cmd == "OR":
			wires[wire] = in1 | in2
		elif cmd == "LSHIFT":
			wires[wire] = in1 << in2
		elif cmd == "RSHIFT":
			wires[wire] = in1 >> in2
	else:
		print("unknown cmd", data)

	# recurse into the dependent wires after successs
	if wire in delayed_wires:
		for item in delayed_wires[wire]:
			process_data(item)
		del delayed_wires[wire]

	return True


for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();

	process_data(data)

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % wires["a"])
