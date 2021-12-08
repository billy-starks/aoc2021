import itertools
from pprint import pprint

def part_1(file):
	data = read_file(file)
	called_numbers = data.pop(0).split(",")
	boards = parse_boards(data)
	for number in called_numbers:
		winning_board = mark_and_check(boards, number)
		if winning_board:
			break
	winning_sum = sum_winning_board(winning_board)
	print("First Winning Board (Marked):")
	pprint(winning_board)
	print(f"Winning Board Sum: {winning_sum}; Last Called Number: {number}")
	return winning_sum * int(number)

def part_2(file):
	data = read_file(file)
	called_numbers = data.pop(0).split(",")
	boards = parse_boards(data)
	last_winning_boards = []
	last_called_number = None
	for number in called_numbers:
		boards, winning_boards = mark_and_check_2(boards, number)
		if winning_boards:
			last_winning_boards = winning_boards
			last_called_number = number
	winning_sum = sum_winning_board(last_winning_boards[0])
	print(f"Last Winning Board (Marked):")
	pprint(last_winning_boards)
	print(f"Winning Board Sum: {winning_sum}; Last Called Number: {last_called_number}")
	return winning_sum * int(last_called_number)


def parse_boards(data):
	boards = []
	while data:
		data.pop(0)
		board = []
		for i in range(5):
			board.append(data.pop(0).split())
		boards.append(board)
	return boards

def mark_and_check(boards, number):
	"""
	Mark boards, then find first winning board
	"""
	for board in boards:
		found_pos = None
		for i, j in itertools.product(range(5), range(5)):
				if board[i][j] == number:
					board[i][j] = "*"
					found_pos = (i,j)
					break
		if found_pos:
			winning = check_board(board, found_pos)
			if winning:
				return board

def mark_and_check_2(boards, number):
	"""
	Mark boards, and return all non-winning and winning boards
	"""
	not_winning_boards = []
	winning_boards = []
	for board in boards:
		found_pos = None
		for i, j in itertools.product(range(5), range(5)):
				if board[i][j] == number:
					board[i][j] = "*"
					found_pos = (i,j)
					break
		if found_pos and check_board(board, found_pos):
			winning_boards.append(board)
		else:
			not_winning_boards.append(board)
	return not_winning_boards, winning_boards
			

def check_board(board, pos):
	i, j = pos
	horizontal = all(board[i][x] == "*" for x in range(5))
	vertical = all(board[y][j] == "*" for y in range(5))
	# unnecessary, read instructions better next time
	# diag = all(board[z][z] == "*" for z in range(5))
	# diag_alt = all(board[z][4-z] == "*" for z in range(5))
	return horizontal or vertical# or diag or diag_alt

def sum_winning_board(board):
	sum = 0
	for i, j in itertools.product(range(5), range(5)):
		sum += 0 if board[i][j] == "*" else int(board[i][j])
	return sum


def read_file(file):
	with open(file, 'r') as data:
		lines = [line.strip() for line in data.readlines()]
	return lines

print(part_1("input.txt"))
print("\n\n")
print(part_2("input.txt"))