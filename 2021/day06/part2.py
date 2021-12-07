from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

# exponential growth, every 7 days, after 0
# unsynchronized
# +2 day before first cycle

memo = {} # global const
def solve_babies(days, initial_clock, spawn_clock, cycle):
	if initial_clock > days:
		return 0

	key = (days, initial_clock)
	if key in memo:
		return memo[key]


	# sync to first cycle and spawn 
	days -= initial_clock
	count = 1 + solve_babies(days, spawn_clock, spawn_clock, cycle)

	# if still enough for more cycles, recurse further
	while days >= cycle:
		days -= cycle
		count += 1 + solve_babies(days, spawn_clock, spawn_clock, cycle)


	memo[key] = count
	return count

spawn = 9
cycle = 7
days = 80

result = 0
for initial_clock in file.readlines()[0].split(","):
	initial_clock = int(initial_clock) + 1 # converting so that spawn happens on 0th day instead of after
	result += 1 + solve_babies(days, initial_clock, spawn, cycle)



print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)