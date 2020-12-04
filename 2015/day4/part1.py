from timeit import default_timer as timer
import hashlib

start = timer()
file = open('input.txt')

inputval = file.readlines()[0]
testhex = ""
num = -1
while testhex[0:5] != "00000":
	num += 1
	testhex = hashlib.md5("%s%d"%(inputval, num)).hexdigest()

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result, with hex %s" % (num, testhex))