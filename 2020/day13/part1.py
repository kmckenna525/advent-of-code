from timeit import default_timer as timer

start = timer()
file = open('input.txt')

lines = file.readlines()
estimate = int(lines[0].strip())
ids = lines[1].strip().split(",")
soonest_wait = None
soonest_id = None
for bus in ids:
	if bus == "x":
		continue
	bus_id = int(bus)
	next_time = (int(estimate/bus_id) + 1) * bus_id
	wait = next_time - estimate
	if soonest_wait is None or wait < soonest_wait:
		soonest_wait = wait
		soonest_id = bus_id

result = soonest_wait * soonest_id
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)