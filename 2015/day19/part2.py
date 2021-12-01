from timeit import default_timer as timer

class Replacement:
	def __init__(self, target, val):
		self.target = target
		self.val = val

	def __str__(self):
		return  "%s => %s" % (self.target, self.val)

	def __repr__(self):
		return  "%s => %s" % (self.target, self.val)

	def get_replacements(self, s):
		length = len(self.target)
		for i in range(len(s)):
			if s[i:i+length] == self.target:
				yield s[0:i] + self.val + s[i+length:]

start = timer()
file = open('input.txt')
replacements = []

medicine = None
state = 0
for line in file.readlines():
	line = line.strip()

	if line == "":
		state += 1

	if state == 0:
		transformation = line.split(" => ")
		replacements.append(Replacement(transformation[0], transformation[1]))
	elif state == 1:
		medicine = line
	

result = 0
while medicine != 'e':
    for replacement in replacements:
        if replacement.val in medicine:
            medicine = medicine.replace(replacement.val, replacement.target, 1)
            result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)