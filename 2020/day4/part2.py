from timeit import default_timer as timer
import re

hgtPattern = r"(?P<val>\d+)(?P<unit>.+)";
def validateHeight(hgt): 
	matches = re.match(hgtPattern, hgt)
	data = matches.groupdict();

	val = int(data["val"])
	unit = data["unit"]

	if(unit == "cm"):
		return val >= 150 and val <= 193
	if(unit == "in"):
		return val >= 59 and val <= 76
	return False

hclPattern = r"^#[0-9a-f]{6}$";

ecls = ["amb","blu","brn","gry","grn","hzl","oth"]

pidPattern = r"^\d{9}$";


required = {
	"byr": lambda x: int(x) >= 1920 and int(x) <= 2002,
	"iyr": lambda x: int(x) >= 2010 and int(x) <= 2020,
	"eyr": lambda x: int(x) >= 2020 and int(x) <= 2030,
	"hgt": validateHeight,
	"hcl": lambda x: re.match(hclPattern, x),
	"ecl": lambda x: x in ecls,
	"pid": lambda x: re.match(pidPattern, x)
}

def validatePassport(passport):
	for field in required.items():
		if field[0] not in passport:
			return False
		if not field[1](passport[field[0]]):
			# print("%s for %s invalid" % (passport[field[0]], field[0]))
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