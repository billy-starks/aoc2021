def part_1(file):
	positions = read_file(file)
	min_x = min(positions)
	max_x = max(positions)
	all_costs = [align_cost(positions, x) for x in range(min_x, max_x + 1)]
	return(min(all_costs))

def part_2(file):
	positions = read_file(file)
	min_x = min(positions)
	max_x = max(positions)
	all_costs = [align_cost_2(positions, x, triangle_range=max_x-min_x) for x in range(min_x, max_x + 1)]
	return(min(all_costs))

def align_cost(positions, x):
	cost = 0
	for pos in positions:
		cost += abs(pos - x)
	return cost

def align_cost_2(positions, x, triangle_range):
	cost = 0
	triangle_numbers = {}
	triangle = 0
	for i in range(triangle_range + 1):
		triangle += i
		triangle_numbers[i] = triangle
	for pos in positions:
		cost += triangle_numbers[abs(pos - x)]
	return cost

def read_file(file):
	with open(file, 'r') as data:
		line = data.read()
	numbers = [int(string) for string in line.split(',')]
	return numbers

print(part_1("input.txt"))
print(part_2("input.txt"))