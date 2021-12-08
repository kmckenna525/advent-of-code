from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

# 7 segment display
#
# ideally
#  aaa
# b   c
# b   c
#  ddd
# e   f
# e   f
#  ggg
#
# 0 = abcefg  (6)
# 1 = cf      (2) *
# 2 = acdeg   (5)
# 3 = acdfg   (5)
# 4 = bcdf    (4) *
# 5 = abdfg   (5)
# 6 = abdefg  (6)
# 7 = acf     (3) *
# 8 = abcdefg (7) *
# 9 = abcdfg  (6)

def get_easy_number(signal):
	count = len(signal)
	if(count == 2):
		return 1
	if(count == 3):
		return 7
	if(count == 4):
		return 4
	if(count == 7):
		return 8
	return None


def get_hard_number(signal, known): # 1, 4, 7, 8 are already known guaranteed
	count = len(signal)
	if(count == 5): # 2, 3, or 5
		# if contains 1, it's 3
		if known[1].shared(signal):
			return 3

		# if it overlaps with 4 with 3 values, it's a 5 (2 is only 1)
		if known[4].share_count(signal) == 3:
		 	return 5

		 # otherwise 0
		return 2

	if(count == 6): # 0, 6, or 9
		# if doesn't contain 1, it's 6 (could use 7, but 1 is quicker)
		if not known[1].shared(signal):
			return 6

		# if it contains 4, it's a 9
		if known[4].shared(signal):
		 	return 9

		 # otherwise 0
		return 0

	# not enough info yet??
	print("This might be an error, but we fell through on %s" % signal)
	return None


def hash_signal(signal):
	return "".join(sorted(signal))


class SignalReader:
	def __init__(self):
		self.number_map = {}
		self.signal_map = {}
		self.pending = []

	def __str__(self):
		return  str(self.number_map)

	def __repr__(self):
		return  str(self.number_map)

	def lookup(self, signal):
		return self.signal_map[hash_signal(signal)]

	def add_to_map(self, num, signal):
		entry = Entry(num, signal)
		self.number_map[num] = entry
		self.signal_map[hash_signal(signal)] = entry

	def incorporate(self, signal):
		if len(self.number_map) >= 4: # if easy all populated
			num = get_hard_number(signal, self.number_map)
			if num is not None:
				self.add_to_map(num, signal)
			return

		num = get_easy_number(signal)
		if num is not None:
			self.add_to_map(num, signal)
			if len(self.number_map) >= 4: # process the deferred ones
				self.process_pending()
			return

		# it's None, so defer calculation
		self.pending.append(signal)

	def process_pending(self):
		for signal in self.pending:
			self.incorporate(signal)

	def read(self, output):
		total = 0
		for signal in output:
			total *= 10
			total += self.lookup(signal).number

		return total



class Entry:
	def __init__(self, number, signal):
		self.number = number
		self.signal = signal
		self.count = len(signal)

	def __str__(self):
		return  "[%d: %s]" % (self.number, self.signal)

	def __repr__(self):
		return  "[%d: %s]" % (self.number, self.signal)

	@property
	def wires(self):
		for wire in self.signal:
			yield wire

	def shared(self, other_signal):
		for wire in self.wires:
			if wire not in other_signal:
				return False
		return True

	def share_count(self, other_signal):
		count = 0
		for wire in self.wires:
			if wire in other_signal:
				count += 1
		return count



result = 0
for line in file.readlines():
	parts = line.strip().split(" | ")
	numbers = parts[0].split(" ")
	output = parts[1].split(" ")

	reader = SignalReader()
	for signal in numbers:
		reader.incorporate(signal)

	result += reader.read(output)


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)