from timeit import default_timer as timer

rules = {}

# rule types
BASE = 0
REF = 1
THEN = 2
OR = 3

def try_parse_int(token):
	try:
		return int(token)
	except:
		return None


def check(text):
	print "text length %d" % len(text)
	a = rules["42"]

	freeze = text[:]
	max42 = 0
	while a.check(freeze, 1):
		# print freeze
		max42 += 1

	if max42 == 0:
		return False

	print max42
	for n in range(1, max42 + 1):
		for m in range(1, n):
			freeze = text[:]
			if checknm(freeze, n, m):
				return True

	return False

# check (42 n + m times) (31 m times)
# check 42 42 31
# check 42 42 42 31 31
# check 42 42 42 42 31 31 31 etc.
def checknm(text, n, m):
	a = rules["42"]
	b = rules["31"]
	# print a.expected_length()
	# print b.expected_length()

	for i in range(0, n + m):
		a.check(text)

	# print text
	for i in range(0, m):
		if not b.check(text):
			print "%d + %d failed at %d" % (n, m, i)
			return False


	print "remaining %d" % len(text)
	return len(text) == 0

class Rule:
	def __init__(self, text):
		self.method = None
		self.val = None
		self.parse(text)

	def parse(self, text):
		# print text

		ors = text.split("|")
		if len(ors) > 1:
			# print "ors"
			self.method = OR
			self.val = []
			for subtext in ors:
				self.val.append(Rule(subtext.strip()))
			# print "ore"
			return

		if "\"" in text:
			# print "base"
			self.method = BASE
			self.val = text.replace("\"","")
			return

		self.val = try_parse_int(text)
		if self.val is not None:
			# print "ref"
			self.val = text
			self.method = REF
			return

		# print "thens"
		subrules = text.split(" ")
		self.method = THEN
		self.val = []
		for subtext in subrules:
			self.val.append(Rule(subtext))
		# print "thene"

	def __repr__(self):
		if self.method == BASE:
			return str(self.val)
		if self.method == REF:
			return str(self.val)
		if self.method == THEN:
			s = ""
			for sub in self.val:
				s += " " + repr(sub)
			return s[1:]
		if self.method == OR:
			s = ""
			for sub in self.val:
				s += " | " + repr(sub)
			return s[3:]

	def expected_length(self):
		if self.method == BASE:
			return (1,1)
		if self.method == REF:
			return rules[self.val].expected_length()
		if self.method == THEN:
			totalmin = 0
			totalmax = 0
			for subrule in self.val:
				val = subrule.expected_length()
				totalmin += val[0]
				totalmax += val[1]
			return (totalmin, totalmax)
		if self.method == OR:
			totalmin = None
			totalmax = None
			for subrule in self.val:
				val = subrule.expected_length()
				if totalmin is None or val[0] < totalmin:
					totalmin = val[0]
				if totalmax is None or val[1] > totalmax:
					totalmax = val[1]
			return (totalmin, totalmax)


	def check(self, text, depth = 0):
		if len(text) == 0:
			return False

		# print " " * depth + str(self)
		# print " " * depth + "test " + "".join(text)

		if self.method == BASE:
			return self.val == text.pop(0)
		if self.method == REF:
			ref = rules[self.val]
			return ref.check(text, depth + 1)
		if self.method == THEN:
			for subrule in self.val:
				if not subrule.check(text, depth + 1):
					return False
			return True
		if self.method == OR:
			freeze = text[:]
			for subrule in self.val:
				# print " " * depth + "or " + str(subrule)
				if subrule.check(freeze, depth + 1):
					# consume same amount of chars
					while len(freeze) != len(text):
						text.pop(0)
					return True
				freeze = text[:]
			return False






start = timer()
file = open('input.txt')

lines = file.readlines()
while len(lines) > 0:
	line = lines.pop(0).strip()
	if line.strip() == "":
		break

	split = line.split(":")
	# if split[0] == "8":
	# 	# print line
	# 	split[1] = "42 | 42 8"
	# if split[0] == "11":
	# 	# print line
	# 	split[1] = "42 31 | 42 11 31"
	# print line
	rules[split[0]] = Rule(split[1].strip())


result = 0
for line in lines:
	checker = list(line.strip())
	# print line.strip()
	passed = check(checker)
	if passed:
		print line
		result += 1
	# print



print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)