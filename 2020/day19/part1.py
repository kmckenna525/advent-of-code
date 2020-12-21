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


	def check(self, text):
		if self.method == BASE:
			return self.val == text.pop(0)
		if self.method == REF:
			ref = rules[self.val]
			return ref.check(text)
		if self.method == THEN:
			for subrule in self.val:
				if not subrule.check(text):
					return False
			return True
		if self.method == OR:
			freeze = text[:]
			for subrule in self.val:
				if subrule.check(freeze):
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
	rules[split[0]] = Rule(split[1].strip())


result = 0
rule = rules["0"]
for line in lines:
	checker = list(line.strip())
	# print checker
	passed = rule.check(checker)
	if passed and len(checker) == 0:
		result += 1



print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)