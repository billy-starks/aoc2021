from itertools import combinations, permutations
from collections import defaultdict
from pprint import pprint
from operator import itemgetter

def read_file(file):
	scanners_data = []
	with open(file, 'r') as data:
		lines = data.readlines()

	for line in lines:
		if line[0:3] == '---': # New scanner
			scanners_data.append([])
		elif len(line) > 1: # Coordinates
			x,y,z = map(int, line.split(","))
			scanners_data[-1].append((x,y,z))
		else: # Newline
			continue
	return scanners_data

def build_deltas(scanner):
	deltas = set()
	for coord1, coord2 in combinations(scanner, 2):
		deltas.add(CoordinateDelta(coord1, coord2))
	return deltas


class CoordinateDelta:
	def __init__(self, coord1, coord2):
		self.coord1 = coord1
		self.coord2 = coord2
		self.x_delta = coord2[0] - coord1[0]
		self.y_delta = coord2[1] - coord1[1]
		self.z_delta = coord2[2] - coord1[2]

	def deltas(self):
		return (self.x_delta, self.y_delta, self.z_delta)

	def coords(self):
		return self.coord1, self.coord2

	def __hash__(self):
		orientation_invariant_sum = sum(map(abs, self.deltas()))
		return hash(orientation_invariant_sum)

	def __eq__(self, other):
		if type(other) is type(self):
			return self.is_match(other)
		return False

	def __str__(self):
		return f"Delta: {self.deltas()}"

	def __repr__(self):
		return self.__str__()
		#return f"CoordinateDelta({self.coord1}, {self.coord2})"

	# Test if this delta matches the other delta in any orientation
	def is_match(self, other):
		other_deltas = set(other.deltas())
		for pos_deltas in self.deltas():
			other_deltas.discard(pos_deltas)
		for neg_deltas in [-delta for delta in self.deltas()]:
			other_deltas.discard(neg_deltas)
		return len(other_deltas) == 0

# Return a function that will map j-coordinates to i-coordinates
def adjust_coordinates(overlap_coords, i, j):
	coordsi = sorted(overlap_coords[i][j])
	coordsj = sorted(overlap_coords[j][i])
	i_x = sorted([coord[0] for coord in coordsi])
	i_y = sorted([coord[1] for coord in coordsi])
	i_z = sorted([coord[2] for coord in coordsi])
	j_x = sorted([coord[0] for coord in coordsj])
	j_y = sorted([coord[1] for coord in coordsj])
	j_z = sorted([coord[2] for coord in coordsj])
	i_components = [i_x, i_y, i_z]
	x_orientations = [component_matches(j_x, x) for x in i_components]
	y_orientations = [component_matches(j_y, x) for x in i_components]
	z_orientations = [component_matches(j_z, x) for x in i_components]
	reoriented_coordsj = sorted(reorient(coord, x_orientations, y_orientations, z_orientations) 
						  for coord in coordsj)

	# Offset is distance from (re-oriented) j-coords to i-coords
	# (From scanner j to scanner i: Position of scanner j in i-coordniates)
	offset = list((coordsi[0][i] - reoriented_coordsj[0][i]) for i in range(3))
	return return_adjustment_function(x_orientations, y_orientations, z_orientations, offset)

# Return true if the difference between each element of each sorted component list is the same
def component_matches(comp1, comp2):
	ncomp2 = sorted([-x for x in comp2])
	return (1 if all((comp1[i] - comp1[i+1]) == (comp2[i] - comp2[i+1]) for i in range(len(comp1) - 1)) else
		   -1 if all((comp1[i] - comp1[i+1]) == (ncomp2[i] - ncomp2[i+1]) for i in range(len(comp1) - 1)) else
		   0)

def reorient(coord, x_orientations, y_orientations, z_orientations):
	new_coord = [0,0,0]
	for i in range(3):
		new_coord[i] = coord[0]*x_orientations[i] + coord[1]*y_orientations[i] + coord[2]*z_orientations[i]
	return new_coord

def make_zero_funcs(adjustment_funcs):
	to_zero_compose = list(adjustment_funcs[0].keys())
	while to_zero_compose:
		current = to_zero_compose.pop()
		for neighbor in list(adjustment_funcs[current].keys()):
			if 0 in adjustment_funcs[neighbor]:
				continue
			adjustment_funcs[neighbor][0] = return_compose_function(adjustment_funcs, neighbor, current)
			to_zero_compose.append(neighbor)
	return adjustment_funcs

def return_adjustment_function(x_orientations, y_orientations, z_orientations, offset):
	def adjustment_func(coord):
		new_coord = reorient(coord, x_orientations, y_orientations, z_orientations)
		new_coord = tuple(new_coord[i] + offset[i] for i in range(3))
		return new_coord
	return adjustment_func

def return_compose_function(adjustment_funcs, neighbor, current):
	def composed_function(coords):
		value = adjustment_funcs[neighbor][current](coords)
		value = adjustment_funcs[current][0](value)
		return value
	return composed_function

def get_all_adjustment_functions_and_data(file):
	scanners_data = read_file(file)
	deltas = list(map(build_deltas, scanners_data))
	overlap_coords = defaultdict(lambda: defaultdict(set))

	# Find overlapping coordinates for each scanner
	for i, deltas_i in enumerate(deltas):
		for j, deltas_j in enumerate(deltas):
			if i == j:
				continue
			# Important that intersection only contains elements from scanner i, since
			# only delta from scanner i have the scanner-i coordinates
			intersection = set(delta for delta in deltas_i if delta in deltas_j)
			coords_in_intersection = set()
			coords_in_intersection.update(delta.coord1 for delta in intersection)
			coords_in_intersection.update(delta.coord2 for delta in intersection)
			if len(coords_in_intersection) >= 12:
				overlap_coords[i][j] = coords_in_intersection

	# Build full list of beacon coordinates relative to scanner 0's position
	adjustment_funcs = defaultdict(lambda: defaultdict(dict))
	all_coordinates = set(scanners_data[0])
	for i in overlap_coords:
		for j in overlap_coords[i]:
			adjustment_funcs[j][i] = adjust_coordinates(overlap_coords, i, j)

	# Compose adjustment functions to ensure every scanner can be readjusted in terms of
	# scanner zero
	adjustment_funcs = make_zero_funcs(adjustment_funcs)
	return adjustment_funcs, scanners_data

def manhattan_distance(coord1, coord2):
	sum = 0
	for i in range(3):
		sum += abs(coord2[i] - coord1[i])
	return sum

def part_1(file):
	adjustment_funcs, scanners_data = get_all_adjustment_functions_and_data(file)
	
	# Built list of all coordinates, adjusting coordinates relative to scanner zero
	all_beacons = set()
	for i in range(len(scanners_data)):
		for coords in scanners_data[i]:
			adjusted_coords = adjustment_funcs[i][0](coords)
			all_beacons.add(adjusted_coords)

	return len(all_beacons)

def part_2(file):
	adjustment_funcs, scanners_data = get_all_adjustment_functions_and_data(file)
	zero = (0,0,0)
	scanner_locations = [adjustment_funcs[i][0](zero) for i in range(len(scanners_data))]
	return max(manhattan_distance(coord1, coord2) for coord1, coord2 in combinations(scanner_locations, 2))



print(part_1("input.txt"))
print(part_2("input.txt"))