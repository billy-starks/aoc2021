def part_1(file):
	data = read_file(file)
	count = len(data)
	mid = count / 2

	one_count_dict = do_one_count(data)
	gamma = ""
	epsilon = ""
	for pos, one_count in one_count_dict.items():
		gamma += ("1" if one_count > mid else "0") 
		epsilon += ("0" if one_count > mid else "1")
	print(f"Gamma: {gamma} ({int(gamma, 2)}); Epsilon: {epsilon} ({int(epsilon, 2)})")
	return int(gamma, 2) * int(epsilon, 2)

def part_2(file):
	data = read_file(file)
	oxygen_rating = generate(data, keep_most=True)
	co2_rating = generate(data, keep_most=False)
	oxygen_rating_decimal = int(oxygen_rating, 2)
	co2_rating_decimal = int(co2_rating, 2)
	print(f"Oxygen Rating: {oxygen_rating} ({oxygen_rating_decimal}); CO2 Rating: {co2_rating} ({co2_rating_decimal})")
	return oxygen_rating_decimal * co2_rating_decimal


def read_file(file):
	with open(file, 'r') as data:
		lines = [line.strip() for line in data.readlines()]
	return lines

def do_one_count(data):
	# Count the number of 1's for each bit position
	# Bit position to count-of-1's dictionary
	one_count_dict = {}
	for line in data:
		pos = 0
		while pos < len(line):
			one_count_dict[pos] = one_count_dict.get(pos, 0) + (1 if line[pos] == "1" else 0)
			pos += 1
	return one_count_dict

def generate(data, keep_most, pos=0):
	mid = len(data) / 2
	one_count_dict = do_one_count(data)
	more_ones = one_count_dict[pos] > mid
	more_zeroes = one_count_dict[pos] < mid
	bit_to_keep = "1" if ((more_ones and keep_most) or (more_zeroes and not keep_most) or (not more_ones and not more_zeroes and keep_most)) else "0"
	filtered_data = [line for line in data if line[pos] == bit_to_keep]
	if len(filtered_data) == 1:
		return filtered_data[0]
	return generate(filtered_data, keep_most, pos+1)


print(part_1("./input.txt"))
print(part_2("./input.txt"))