def part_1(file):
	grid, fold_insts = read_file(file)
	axis, pos = fold_insts[0]
	fold(grid, fold_axis=axis, fold_pos=pos)
	return(len(grid))

def part_2(file):
	grid, fold_insts = read_file(file)
	for axis, pos in fold_insts:
		fold(grid, fold_axis=axis, fold_pos=pos)
	print_grid(grid)


def fold(grid, fold_axis, fold_pos):
	coord = 1 if fold_axis == "y" else 0 # coordinate modified by fold
	dots_to_remove = set()
	folded_dots = set()
	for dot in grid:
		if dot[coord] > fold_pos:
			dots_to_remove.add(dot)
			folded_dot = list(dot)
			folded_dot[coord] = fold_pos - (dot[coord] - fold_pos)
			folded_dots.add(tuple(folded_dot))
	grid.difference_update(dots_to_remove)
	grid.update(folded_dots)

def print_grid(grid):
	x_max = max(x for x,y in grid)
	y_max = max(y for x,y in grid)
	string = ""
	for y in range(y_max+1):
		for x in range(x_max+1):
			string += "# " if (x,y) in grid else ". "
		string += '\n'
	print(string)


def read_file(file):
	grid = set()
	fold_insts = []
	with open(file, 'r') as data:
		lines = data.readlines()
	newline_index = lines.index('\n')
	for line in lines[:newline_index]:
		x, y = map(int, line.strip().split(','))
		grid.add((x,y))
	for line in lines[newline_index+1:]:
		axis, pos = line.split()[2].split('=')
		pos = int(pos)
		fold_insts.append((axis,pos))

	return grid, fold_insts

print(part_1("input.txt"))
part_2("input.txt")