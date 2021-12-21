import main
import os
import time
import sys


def animate_image(file, low=-20, high=20, fps=3):
	algo_string, pixel_grid = main.read_file(file)
	while True:
		pixel_grid = main.enhance(algo_string, pixel_grid)
		pixel_grid = resparseify(pixel_grid)
		print_bounded_grid(pixel_grid, low, high)
		time.sleep(1 / fps)
		os.system('clear')

def print_bounded_grid(pixel_grid, low, high):
	string = "".join('-' for _ in range(low -1, high + 2)) + "\n"
	for y in range(low, high+1):
		string += "|"
		for x in range(low, high+1):
			value = pixel_grid[y][x] if y in pixel_grid and x in pixel_grid[y] else pixel_grid.default_factory().default_factory()
			string += "#" if value == 1 else " "
		string += "|"
		string += '\n'
	print(string)

def resparseify(pixel_grid):
	default_value = pixel_grid.default_factory().default_factory()
	new_pixel_grid = main.create_pixel_grid(default_value)
	y_keys = list(pixel_grid.keys())
	for y in y_keys:
		x_keys = list(pixel_grid[y].keys())
		for x in x_keys:
			# Enhance code assume pixel_grid[0] always exists; don't remove it
			if all(pixel_grid[y+j][x+i] == default_value for j in [-1,0,1] for i in [-1,0,1]):
				if y != 0:
					continue
				max_value = max(x_keys)
				min_value = min(x_keys)
				if x not in (min_value, max_value):
					continue
			new_pixel_grid[y][x] = pixel_grid[y][x]
	return new_pixel_grid
  
  
if __name__ == "__main__":
	low = int(sys.argv[1]) if len(sys.argv) > 1 else -10
	high = int(sys.argv[2]) if len(sys.argv) > 2 else 10
	fps = int(sys.argv[3]) if len(sys.argv) > 3 else 3
	file = sys.argv[4] if len(sys.argv) > 4 else "life.txt"
	animate_image(file, low, high, fps)
