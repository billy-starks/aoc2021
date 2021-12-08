from collections import Counter
from pprint import pprint

def part_1(file):
	data = read_file(file)
	line_segment_count = get_line_segment_count(data)
	return sum(x >= 2 for x in line_segment_count.values())

def part_2(file):
	data = read_file(file)
	line_segment_count = get_line_segment_count(data, ignore_diag=False)
	return sum(x >= 2 for x in line_segment_count.values())

def get_line_segment_count(data, ignore_diag=True):
	counter = Counter()
	for datum in data:
		line = get_line_points(datum, ignore_diag)
		for points in line:
			counter[points] += 1
	return counter
		

def get_line_points(datum, ignore_diag=True):
	point1, point2 = datum.split("->")
	x1,y1 = map(int, point1.split(","))
	x2,y2 = map(int, point2.split(","))
	if x1 == x2:
		lowY = min(y1,y2)
		highY = max(y1,y2) + 1
		return [(x1,y) for y in range(lowY, highY)]
	if y1 == y2:
		lowX = min(x1,x2)
		highX = max(x1,x2) + 1
		return [(x,y1) for x in range(lowX, highX)]
	else:
		if ignore_diag:
			return []
		else:
			lowY = min(y1,y2)
			highY = max(y1,y2) + 1
			polarity_y = 1 if (lowY == y1) else -1
			lowX = min(x1,x2)
			highX = max(x1,x2) + 1
			polarity_x = 1 if (lowX == x1) else -1
			return_list = []
			for i in range(0, highY - lowY):
				return_list.append((x1 + (polarity_x * i), y1 + (polarity_y * i)))
			return return_list

def read_file(file):
	with open(file, 'r') as data:
		lines = [line.strip() for line in data.readlines()]
	return lines

print(part_1("./input.txt"))
print(part_2("./input.txt"))