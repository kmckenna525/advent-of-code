from timeit import default_timer as timer

start = timer()
file = open('input.txt')

result = 0
seats = []
for line in file.readlines():
	binary = ""
	for char in line:
		if char in ["F","L"]:
			binary += "0"
		if char in ["B","R"]:
			binary += "1"

	seat_id = int(binary, 2)

	seats.append(seat_id)

seats.sort()
last_id = None
for seat_id in seats:
	if last_id and seat_id != last_id + 1: 
		result = seat_id - 1
		break;
	last_id = seat_id

print("Completed in %fms" % ((timer() - start) * 1000))

row = result >> 3
col = result & 0b111
print("row %d, column %d, seat ID %d" % (row, col, result))