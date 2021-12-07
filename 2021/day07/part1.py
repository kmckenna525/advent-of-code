from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

# horizontal positions
# 1 fuel per any one step
# find optimal

def calculate_fuel(positions, target, best = None):
	fuel = 0
	for position in positions:
		fuel += abs(position - target)
		if best is not None and fuel > best:
			return None
	return fuel


target_min = None
target_max = None
positions = []
for pos in file.readlines()[0].split(","):
	pos = int(pos)
	positions.append(pos)
	if target_min is None or pos < target_min:
		target_min = pos
	if target_max is None or pos > target_max:
		target_max = pos


result = None
optimal_target = None
for target in range(target_min, target_max):
	fuel = calculate_fuel(positions, target, result)
	if fuel is not None and (result is None or fuel < result):
		optimal_target = target
		result = fuel


print("Completed in %fms" % ((timer() - start) * 1000))
print("position %d with %d fuel is the result" % (optimal_target, result))