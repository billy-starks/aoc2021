from pprint import pprint

def part_1(file):
	grid = read_file(file)
	low_points = []
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			point = grid[y][x]
			adjacent_points = get_adjancent(grid, (y,x))
			if all(point < adj for adj in adjacent_points):
				low_points.append(point)
	return sum(low_points) + len(low_points)

def part_2(file):
	grid = read_file(file)
	low_points = []
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			point = grid[y][x]
			adjacent_points = get_adjancent(grid, (y,x))
			if all(point < adj for adj in adjacent_points):
				low_points.append((y,x))

	# Identify basin with its most top, then most left point
	# in case there are multiple low points in a single basin
	basin_to_size = {}

	for point in low_points:
		basin_id = point
		basin_current = [point]
		basin = {point}
		y,x = point
		current_value = grid[y][x]
		while basin_current:
			adjacent_points = [adj for cur in basin_current for adj in get_adjancent_points(grid, cur) if adj not in basin]
			basin_current = [adj for adj in adjacent_points if get_flow_point(grid, adj) in basin]
			basin_current = [point for point in basin_current if grid[point[0]][point[1]] != 9]
			for y, x in basin_current:
				if y <= basin_id[0] and x <= basin_id[1]:
					basin_id = (y,x)
				basin.add((y,x))
		basin_to_size[basin_id] = len(basin)

	largest_sizes = sorted(basin_to_size.values())[-3:]
	product = 1
	for size in largest_sizes:
		product *= size
	return product

def read_file(file):
	with open(file, 'r') as data:
		lines = data.readlines()
	grid = [[int(x) for x in line.strip()] for line in lines]
	return grid

def get_adjancent(grid, pos):
	y, x = pos
	points = []
	if y+1 < len(grid):
		points.append(grid[y+1][x])
	if y-1 >= 0:
		points.append(grid[y-1][x])
	if x+1 < len(grid[0]):
		points.append(grid[y][x+1])
	if x-1 >= 0:
		points.append(grid[y][x-1])
	return points

def get_adjancent_points(grid, pos):
	y, x = pos
	points = []
	if y+1 < len(grid):
		points.append((y+1, x))
	if y-1 >= 0:
		points.append((y-1,x))
	if x+1 < len(grid[0]):
		points.append((y,x+1))
	if x-1 >= 0:
		points.append((y,x-1))
	return points

def get_flow_point(grid, pos):
	adj_points = get_adjancent_points(grid, pos)
	flow_point = adj_points[0]
	for adj in adj_points:
		y_cur, x_cur = flow_point
		y_new, x_new = adj
		if grid[y_new][x_new] < grid[y_cur][x_cur]:
			flow_point = adj
	return flow_point

print(part_1("input.txt"))
print(part_2("input.txt"))