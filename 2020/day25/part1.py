from timeit import default_timer as timer

DIV = 20201227
INITIAL_SUBJECT = 7

start = timer()
file = open('input.txt')

def do_transforms(subject, loop_size):
	return pow(subject, loop_size, 20201227)

def find_loop_size(subject, target):
	test = 0
	result = -1
	while result != target:
		test += 1
		result = do_transforms(subject, test)
		# print (test, result)
	return test

lines = file.readlines()
card_key = int(lines[0].strip())
door_key = int(lines[1].strip())

# print (card_key, door_key)
card_loop = find_loop_size(INITIAL_SUBJECT, card_key)
# door_loop = find_loop_size(INITIAL_SUBJECT, door_key)
# print (card_loop, door_loop)

result = do_transforms(door_key, card_loop)
print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)