from timeit import default_timer as timer

required = [
	"byr",
	"iyr",
	"eyr",
	"hgt",
	"hcl",
	"ecl",
	"pid"
]

def validatePassport(passport):
	for field in required:
		if field not in passport:
			return False

	return True


start = timer()
file = open('input.txt')

passport = {}
result = 0
for line in file.readlines():
	if(line == "\n"):
		if validatePassport(passport):
			result += 1
		passport = {}
		continue

	kvps = line.split()
	for kvp in kvps:
		kvpSplit = kvp.split(":")
		passport[kvpSplit[0]] = kvpSplit[1]

if validatePassport(passport):
	result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)