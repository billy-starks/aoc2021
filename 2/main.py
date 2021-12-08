def part_1(file):
	lines = read_file(file)
	depth = 0
	X = 0
	for line in lines:
		direction, amount = line.split(" ")
		amount = int(amount)
		if direction == "down":
			depth += amount
		if direction == "up":
			depth -= amount
		if direction == "forward":
			X += amount
	print(f"Depth: {depth}, X: {X}")
	return depth * X

def part_2(file):
	lines = read_file(file)
	depth = 0
	X = 0
	aim = 0
	for line in lines:
		direction, amount = line.split(" ")
		amount = int(amount)
		if direction == "down":
			aim += amount
		if direction == "up":
			aim -= amount
		if direction == "forward":
			X += amount
			depth += (aim * amount)
	print(f"Depth: {depth}, X: {X}")
	return depth * X

def read_file(file):
	with open(file, 'r') as data:
		lines = [line for line in data.readlines()]
	return lines

print(part_1("input.txt"))
print(part_2("input.txt"))