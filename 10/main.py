import statistics

OPEN_TO_CLOSE = {
	'{': '}',
	'[': ']',
	'(': ')',
	'<': '>'
}

CLOSE_TO_SCORE = {
	')': 3,
	']': 57,
	'}': 1197,
	'>': 25137
}

CLOSE_TO_SCORE_2 = {
	')': 1,
	']': 2,
	'}': 3,
	'>': 4
}

def part_1(file):
	lines = read_file(file)
	illegal_chars = []
	for line in lines:
		illegal_char = check_illegal_char(line)
		if illegal_char:
			illegal_chars.append(illegal_char)
	return sum(CLOSE_TO_SCORE[char] for char in illegal_chars)

def part_2(file):
	lines = read_file(file)
	completions = []
	for line in lines:
		illegal_char = check_illegal_char(line)
		if illegal_char:
			continue
		completions.append(complete_line(line))
	return statistics.median(score_completion(completion) for completion in completions)



def check_illegal_char(line):
	stack = []
	for char in line:
		# Push opening chars on stack
		if char in OPEN_TO_CLOSE:
			stack.append(char)
		else: # Check closing char matches last on stack
			if OPEN_TO_CLOSE[stack.pop()] != char:
				return char
	return None

def complete_line(line):
	stack = []
	for char in line:
		# Push opening chars on stack
		if char in OPEN_TO_CLOSE:
			stack.append(char)
		else: # Assume closing character matches last on stack
			stack.pop()
	return "".join(OPEN_TO_CLOSE[char] for char in reversed(stack))

def score_completion(completion):
	score = 0
	for char in completion:
		score *= 5
		score += CLOSE_TO_SCORE_2[char]
	return score


def read_file(file):
	with open(file, 'r') as data:
		lines = data.readlines()
	return [line.strip() for line in lines]

print(part_1("input.txt"))
print(part_2("input.txt"))