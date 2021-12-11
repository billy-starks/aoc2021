from pprint import pprint

def part_1(file):
	grid = read_file(file)
	flash_count = 0
	for _ in range(100):
		flash_count += step_grid(grid)
	pprint(grid)
	return flash_count

def part_2(file):
	grid = read_file(file)
	step_count = 0
	while True:
		step_count += 1
		if step_grid(grid) == 100:
			return step_count


def step_grid(grid):
	# First, the energy level of each octopus increases by 1
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			grid[y][x] += 1

	# Then, any octopus with an energy level greater than 9 flashes.
	# This increases the energy level of all adjacent octopuses by 1
	flashed = set()
	check_for_flash = set((y,x) for y in range(len(grid)) for x in range(len(grid[0])))
	while check_for_flash:
		coords = check_for_flash.pop()
		y, x = coords
		if grid[y][x] > 9 and coords not in flashed:
			flashed.add(coords)
			for adj_coords in get_adjacent_coordinates(grid, coords):
				y_adj, x_adj = adj_coords
				grid[y_adj][x_adj] += 1
				check_for_flash.add(adj_coords)

	# Finally, any octopus that flashed during this step has its energy level set to 0
	for y, x in flashed:
		grid[y][x] = 0

	# Get number of octopus that flashed
	return len(flashed)

def get_adjacent_coordinates(grid, coords):
	y, x = coords
	potential_coords = [(y-1,x-1), (y,x-1), (y+1,x-1),
						(y-1,x), (y,x), (y+1,x),
						(y-1,x+1), (y,x+1), (y+1,x+1)]
	return [adj for adj in potential_coords if (0 <= adj[0] < len(grid) and 0 <= adj[1] < len(grid[0]))]



def read_file(file):
	with open(file, 'r') as data:
		grid = [[int(num) for num in line.strip()] for line in data.readlines()]
	return grid

print(part_1("input.txt"))
print(part_2("input.txt"))