def part_1(file, print_debug=False):
	with open(file, 'r') as data:
		lines = [int(line) for line in data.readlines()]
	total_increases = 0
	for index in range(len(lines) - 1):
		if lines[index+1] > lines[index]:
			total_increases += 1
	return total_increases

def part_2(file, print_debug=False):
	with open(file, 'r') as data:
		lines = [int(line) for line in data.readlines()]
	total_increases = 0
	for index in range(len(lines) - 3):
		if lines[index+3] > lines[index]:
			total_increases += 1
	return total_increases



print(part_1("./input.txt"))
print(part_2("./input.txt"))