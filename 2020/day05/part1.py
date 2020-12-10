from timeit import default_timer as timer

start = timer()
file = open('input.txt')

highest = 0
for line in file.readlines():
	binary = ""
	for char in line:
		if char in ["F","L"]:
			binary += "0"
		if char in ["B","R"]:
			binary += "1"

	seat_id = int(binary, 2)
	row = seat_id >> 3
	col = seat_id & 0b111

	if seat_id > highest:
		highest = seat_id

	# print("row %d, column %d, seat ID %d" % (row, col, seat_id))

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the highest" % highest)