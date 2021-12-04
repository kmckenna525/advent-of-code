from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')


class BoardKey:
	def __init__(self, row, column):
		self.row = row
		self.column = column

	def __str__(self):
		return  "[[%d, %d]]" % (self.row, self.column)

	def __repr__(self):
		return  "[[%d, %d]]" % (self.row, self.column)

	def increment(self, size):
		column = self.column + 1
		row = self.row
		if column >= size:
			column = 0
			row += 1
		return BoardKey(row, column)


class Board:
	def __init__(self, board_id, size):
		self.id = board_id
		self.board = []
		for i in range(0, size):
			self.board.append([False] * size)
		self.ids = {}
		self.next_key = BoardKey(0,0)
		self.size = size

	def __str__(self):
		return "%d(%d): %s" % (self.id, self.remaining(), str(self.board))

	def __repr__(self):
		return "%d(%d): %s" % (self.id, self.remaining(), str(self.board))

	def debug(self):
		board = []
		for i in range(0, self.size):
			board.append([None] * self.size)

		for num, key in self.ids.items():
			board[key.row][key.column] = num

		print board


	def init_next(self, num):
		key = self.next_key
		self.ids[num] = key
		self.next_key = key.increment(self.size)

	def mark(self, num):
		if num not in self.ids:
			return False
		key = self.ids[num]
		self.board[key.row][key.column] = True
		return True

	def is_row_bingo(self, row):
		for column in range(0, self.size):
			if not self.board[row][column]:
				return False
		return True

	def is_column_bingo(self, column):
		for row in range(0, self.size):
			if not self.board[row][column]:
				return False
		return True

	def is_bingo(self):
		for i in range(0, self.size):
			if self.is_row_bingo(i):
				return True
			if self.is_column_bingo(i):
				return True

		return False

	def remaining(self):
		total = 0
		for num, key in self.ids.items():
			if not self.board[key.row][key.column]:
				total += int(num)
		return total

def check_call(call, boards):
	for board in boards:
		board.mark(call)
		if board.is_bingo():
			return board
	return None
		

boards = [] 

lines = file.readlines()

dim = 5
calls = lines[0].strip().split(",")
current_board = Board(0,dim)
boards.append(current_board)
for line in lines[2:]:
	row = line.strip().split()
	if len(row) == 0:
		current_board = Board(len(boards),dim)
		boards.append(current_board)

	for entry in row:
		current_board.init_next(entry)

result = 0
for call in calls:
	winner = check_call(call, boards)
	if winner is not None:
		print call, winner
		result = int(call) * winner.remaining()
		break

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)




















