from timeit import default_timer as timer

config = {
	"straight": 3,
	"exclude": set(["i","o","l"]),
	"pairs": 2,
}

num_to_char = "abcdefghijklmnopqrstuvwxyz"
char_to_num = {}
for i in range(0, len(num_to_char)):
	char_to_num[num_to_char[i]] = i

def convert_to_char(pass_as_num):
	password = ""
	for num in pass_as_num:
		password += num_to_char[num]
	return password

def convert_to_num(password):
	pass_as_num = []
	for char in password:
		pass_as_num.append(char_to_num[char])
	return pass_as_num

def increment(pass_as_num, index):
	if index < 0:
		pass_as_num.insert(0, 1)
		return
	for i in range(index + 1, len(pass_as_num)):
		pass_as_num[i] = 0
	pass_as_num[index] = (pass_as_num[index] + 1)
	if pass_as_num[index] >= len(num_to_char):
		pass_as_num[index] = 0
		increment(pass_as_num, index - 1)

def check_exclude(password):
	for i in range(0,len(password)):
		char = password[i]
		if char in config["exclude"]:
			return i
	return -1

def check_straight(pass_as_num):
	prev = pass_as_num[0]
	count = 1
	for num in pass_as_num[1:]:
		if num == prev + 1:
			count += 1
		else:
			count = 1
		prev = num
		if count >= config["straight"]:
			break
	return count >= config["straight"]

def check_pairs(password):
	pairs = set()
	prev = password[0]
	for char in password[1:]:
		if char == prev:
			pairs.add(prev)
			continue
		prev = char
	return len(pairs) >= config["pairs"]
		


start = timer()
file = open('input.txt')

password = file.readlines()[0].strip()
pass_as_num = convert_to_num(password)
increment(pass_as_num, len(pass_as_num) - 1)

while True:
	index = check_exclude(password)
	if index >= 0:
		# print "not allowed"
		increment(pass_as_num, index)
	elif not check_straight(pass_as_num):
		# print "no straight"
		increment(pass_as_num, len(pass_as_num) - 1)
	elif not check_pairs(password):
		# print "no pairs"
		increment(pass_as_num, len(pass_as_num) - 1)
	else:
		# print "good"
		break;
	password = convert_to_char(pass_as_num)
	# print password

result = password

print("Completed in %fms" % ((timer() - start) * 1000))
print("%s is the result" % result)