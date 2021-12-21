from collections import defaultdict
from pprint import pprint

def read_file(file):
	with open(file, 'r') as data:
		lines = data.readlines()
	algo_string = lines[0]
	# Pixel grid is a sparse grid; represents infinite grid mostly filled with 0's
	pixel_grid = create_pixel_grid(0)
	for y, line in enumerate(lines[2:]):
		for x, char in enumerate(line.strip()):
			pixel_grid[y][x] = 1 if char == "#" else 0
	return algo_string, pixel_grid

def get_index(pixel_grid, x, y):
	index = 0
	for i,j in [(-1,-1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1,1)]:
		index *= 2
		index += pixel_grid[y+j][x+i]
	return index

def get_index_value(algo_string, index):
	return 1 if algo_string[index] == "#" else 0

def create_pixel_grid(default_value):
	return defaultdict(lambda: defaultdict(lambda: default_value))

def enhance(algo_string, pixel_grid):
	# Pixel grid is full of either mostly 0's or 1's
	# Either one of the two below
	# ...                ###
	# ...                ###
	# ...                ###
	# Create a new sparse grid that defaults to the value chosen
	# at index 0 or 511 by the algorithm
	default_value = pixel_grid.default_factory().default_factory()
	index = 0 if default_value == 0 else (2**9 - 1)
	value = get_index_value(algo_string, index)
	new_pixel_grid = create_pixel_grid(value)

	# Calculate the values of new_pixel_grid whose 3x3 square overlaps
	# any pixel in the 'sparse' part of pixel_grid
	# Eq. If pixel_grid goes from (0,0) to (4,4), calculate all pixels
	# in new_pixel_grid from (-1,-1) to (5,5)
	points_to_check = get_points_to_check(pixel_grid)
	for x,y in points_to_check:
	    index = get_index(pixel_grid, x, y)
	    value = get_index_value(algo_string, index)
	    new_pixel_grid[y][x] = value
	return new_pixel_grid

def get_points_to_check(pixel_grid):
	ys_to_check = list(pixel_grid.keys())
	points_to_check = set()
	for y in ys_to_check:
		for x in list(pixel_grid[y].keys()):
			points_to_check.update(((x+i), (y+j)) for j in [-1,0,1] for i in [-1,0,1])
	return points_to_check

def print_grid(pixel_grid):
	string = ""
	for y in sorted(pixel_grid.keys()):
		for x in sorted(pixel_grid.keys()):
			string += "#" if pixel_grid[y][x] == 1 else "."
		string += '\n'
	print(string)

def part_1(file):
	algo_string, pixel_grid = read_file(file)
	for _ in range(2):
		pixel_grid = enhance(algo_string, pixel_grid)
	count = 0
	for y in pixel_grid:
		for x in pixel_grid[y]:
			if pixel_grid[y][x] == 1:
				count += 1
	return count

def part_2(file):
	algo_string, pixel_grid = read_file(file)
	for _ in range(50):
		pixel_grid = enhance(algo_string, pixel_grid)
	count = 0
	for y in pixel_grid:
		for x in pixel_grid[y]:
			if pixel_grid[y][x] == 1:
				count += 1
	return count

if __name__ == "__main__":
	print(part_1("input.txt"))
	print(part_2("input.txt"))