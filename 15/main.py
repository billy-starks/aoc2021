from pprint import pprint
import sys

def part_1(file):
	grid = read_file(file)
	risk_grid = get_risk_grid_2(grid)
	return risk_grid[-1][-1]

def part_2(file):
	grid = read_file(file)
	risk_grid = get_risk_grid_2(grid, extend=5)
	return risk_grid[-1][-1]

# Dynamic programming was not the way
# def get_risk_grid(grid, extended=1):
# 	risk_grid = [[0 for _ in range(len(grid[0]) * extended)] for _ in range(len(grid) * extended)]
# 	for index_sum in range(1, 2 * extended * len(grid)):
# 		for x,y in generate_indices(index_sum):
# 			if x >= len(grid)*extended or y >= len(grid)*extended:
# 				continue
# 			min_risk = get_min_risk(risk_grid, (x,y))
# 			risk_grid[y][x] = min_risk + get_value(grid, (x, y))
# 	return risk_grid

def get_risk_grid_2(grid, extend=1):
	risk_grid = [[float("inf") for _ in range(len(grid[0]) * extend)] for _ in range(len(grid) * extend)]
	risk_grid[0][0] = 0
	nodes_to_check = set([(0,1), (1,0)])
	while nodes_to_check:
		node = nodes_to_check.pop()
		x, y = node
		min_risk = get_min_risk_2(risk_grid, node)
		new_risk = min_risk + get_value(grid, node)
		if new_risk < risk_grid[y][x]:
			risk_grid[y][x] = new_risk
			nodes_to_check.update(get_neighbor_nodes(grid, node, extend))
	return risk_grid

def get_value(grid, pos):
	offset = 0
	x, y = pos
	num_rows = len(grid)
	num_cols = len(grid[0])
	cur_y = y
	cur_x = x
	while cur_y >= num_rows:
		cur_y -= num_rows
		offset += 1
	while cur_x >= num_cols:
		cur_x -= num_cols
		offset += 1
	return wrap(grid[cur_y][cur_x] + offset)

def generate_indices(index_sum):
	if index_sum == 0:
		yield (0,0)
		return
	x = 0
	y = index_sum
	while y >= 0:
		yield (x,y)
		x += 1
		y -= 1

def get_min_risk(grid, pos):
	x, y = pos
	if x == 0 and y == 0:
		return 0
	if x == 0:
		return grid[y-1][x]
	if y == 0:
		return grid[y][x-1]
	return min(grid[y-1][x], grid[y][x-1])

def get_min_risk_2(grid, pos):
	x, y = pos
	neighbor_risks = [grid[j][i] for i,j in get_neighbor_nodes(grid, pos)]
	return min(neighbor_risks)

def get_neighbor_nodes(grid, pos, extend=1):
	x,y = pos
	return [(i,j) for i,j in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)] if 0 <= i < len(grid[0])*extend and 0 <= j < len(grid)*extend]

def wrap(num):
	while num >= 10:
		return num - 9
	return num


def read_file(file):
	with open(file, 'r') as data:
		lines = data.readlines()
	return [[int(num) for num in line.strip()] for line in lines]

def print_grid(grid):
	string = ''
	for y in range(len(grid)):
		string += ','.join(map(str, grid[y]))
		string += '\n'
	print(string)

print(part_1("input.txt"))
print(part_2("input.txt"))