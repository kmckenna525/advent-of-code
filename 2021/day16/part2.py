from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')


transmission = file.read().strip()

maskmemo = {}
def bitmask(count):
	if count not in maskmemo:
		maskmemo[count] = int("1"*count, 2)

	return maskmemo[count]


class Bitqueue:
	def __init__(self):
		self.val = 0
		self.count = 0

	def __str__(self):
		return bin(self.val)

	def __repr__(self):
		return bin(self.val)

	def push(self, val, count):
		self.val = self.val << count
		self.val |= val
		#print "pushed", bin(self.val), bin(val)
		self.count += count

	def pop(self, count):
		if count > self.count:
			raise Exception("%d out of range for length %d" % (count, self.count))

		self.count -= count
		val = self.val >> self.count

		if self.count == 0:
			self.val = 0
		else:
			self.val = self.val & bitmask(self.count)
		#print "pop", bin(self.val), bin(val)
		return val


class Packet:
	def __init__(self):
		self.state = 0 # 0 = version, 1 = type, 2 = length type id, 3 = length, 4 = subpackets, 5 = done
		self.version = 0
		self.type = 0
		self.meta_length = 0

		self.literal = 0

		self.length_type_id = 0
		self.length = 0
		self.incomplete_subpacket = None
		self.subpackets = []


	def __str__(self):
		if self.isliteral:
			return str((self.version, self.type, self.literal))

		return str((self.version, self.type, self.length_type_id, self.length, self.subpackets))


	def __repr__(self):
		if self.isliteral:
			return str((self.state, self.version, self.type, self.literal))

		return str((self.state, self.version, self.type, self.length_type_id, self.length, self.subpackets))


	@property
	def isliteral(self):
		return self.type == 4


	@property
	def length_bitcount(self):
		return 11 if self.length_type_id == 1 else 15


	@property
	def total_length(self):
		return self.meta_length + self.subpackets_bitlength


	@property
	def subpackets_length(self):
		if self.length_type_id == 1:
			return len(self.subpackets)
		return self.subpackets_bitlength


	@property
	def subpackets_bitlength(self):
		total = 0
		for packet in self.subpackets:
			total += packet.total_length
		return total


	def evaluate(self):
		subpackets = self.subpackets
		if self.type == 0: #sum
			total = 0
			for packet in subpackets:
				total += packet.evaluate()
			return total
		if self.type == 1: #multiply
			total = 1
			for packet in subpackets:
				total *= packet.evaluate()
			return total
		if self.type == 2: #min
			values = []
			for packet in subpackets:
				values.append(packet.evaluate())
			return min(values)
		if self.type == 3: #max
			values = []
			for packet in subpackets:
				values.append(packet.evaluate())
			return max(values)
		if self.type == 4: #literal
			return self.literal
		if self.type == 5: #greater
			a = subpackets[0].evaluate()
			b = subpackets[1].evaluate()
			return 1 if a > b else 0
		if self.type == 6: #less
			a = subpackets[0].evaluate()
			b = subpackets[1].evaluate()
			return 1 if a < b else 0
		if self.type == 7: #equal
			a = subpackets[0].evaluate()
			b = subpackets[1].evaluate()
			return 1 if a == b else 0
		raise Exception("Invalid type %d"%(self.type))


	
	

	# returns True if done, False if not
	def read(self, bitqueue):
		#print "state", self.state
		if self.state == 0:
			self.read_version(bitqueue)
		elif self.state == 1:
			self.read_type(bitqueue)
		elif self.state == 2:
			self.read_lti(bitqueue)
		elif self.state == 3:
			self.read_length(bitqueue)
		elif self.state == 4:
			self.read_subpacket(bitqueue)
		
		return self.state > 4

	def read_version(self, bitqueue):
		if bitqueue.count < 3:
			return
		self.version = bitqueue.pop(3)
		self.meta_length += 3
		self.state += 1

		#print "version", self.version, bin(self.version)


	def read_type(self, bitqueue):
		if bitqueue.count < 3:
			return
		self.type = bitqueue.pop(3)
		self.meta_length += 3
		self.state += 1

		#print "type", self.version, bin(self.version)


	def read_lti(self, bitqueue):
		if self.isliteral:
			self.state += 1
			return

		if bitqueue.count < 1:
			return
		self.length_type_id = bitqueue.pop(1)
		self.meta_length += 1
		self.state += 1

		#print "length_type_id", self.length_type_id, bin(self.length_type_id)


	def read_length(self, bitqueue):
		if self.isliteral:
			self.state += 1
			return

		bitcount = self.length_bitcount
		if bitqueue.count < bitcount:
			return
		self.length = bitqueue.pop(bitcount)
		self.meta_length += bitcount
		self.state += 1

		#print "length", self.length, bin(self.length)


	def read_subpacket(self, bitqueue):
		if self.isliteral:
			self.read_literal(bitqueue)
			return

		self.read_operator_subpacket(bitqueue)


	def read_literal(self, bitqueue):
		if bitqueue.count < 5:
			return
			
		raw = bitqueue.pop(5)
		self.meta_length += 5

		firstbit = raw >> 4
		val = raw & bitmask(4)
		self.literal = self.literal << 4
		self.literal |= val
		if firstbit == 0:
			self.state += 1

	def read_operator_subpacket(self, bitqueue):
		if self.incomplete_subpacket is None:
			self.incomplete_subpacket = Packet()

		if self.incomplete_subpacket.read(queue):
			self.subpackets.append(self.incomplete_subpacket)
			self.incomplete_subpacket = None
			if self.subpackets_length >= self.length:
				self.state += 1


 
queue = Bitqueue()
packet = Packet()
for byte in transmission:
	num = int(byte, 16)
	queue.push(num, 4)

	if packet.read(queue):
		break

while queue.val != 0:
	if packet.read(queue):
		break


result = packet.evaluate()

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)