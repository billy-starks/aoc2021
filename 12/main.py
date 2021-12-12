from collections import defaultdict, Counter
from pprint import pprint
from time import sleep
import string

def part_1(file):
	graph = read_file(file)
	paths = do_search(graph)
	return len(paths)

def is_invalid_path(path):
	small_caves = set()
	for node in path:
		if str.islower(node):
			if node in small_caves:
				return True
			else:
				small_caves.add(node)
	return False

def is_invalid_path_2(path):
	small_caves = Counter()
	for node in path:
		if str.islower(node):
			small_caves[node] += 1
			if (node == 'start' or node == 'end') and (small_caves[node] > 1):
				return True
			if small_caves[node] > 2:
				return True
	caves_visited_twice = 0
	for num_visits in small_caves.values():
		if num_visits >= 2:
			caves_visited_twice += 1
	return not (caves_visited_twice <= 1)

def part_2(file):
	graph = read_file(file)
	paths = do_search(graph, invalid_path_func=is_invalid_path_2)
	return len(paths)

def do_search(graph, invalid_path_func=is_invalid_path):
	next_neighbors = [set(['start'])]
	path = []
	all_paths = []
	while True:
		neighbors = next_neighbors.pop()

		# All of last nodes' neighbors have been visited
		# So backtrack path
		# print(path, '\n', neighbors, '\n')
		if not neighbors:
			if not path:
				break
			path.pop()
			continue

		# Append path with last node in neighbors
		# Add unvisited neighbors back to process at later setp
		path.append(neighbors.pop())
		next_neighbors.append(neighbors)

		# Backtrack immediately if path became invalid
		if invalid_path_func(path):
			path.pop()
			continue

		# If path reaches end, save path and backtrack
		if path[-1] == 'end':
			all_paths.append("-".join(path))
			path.pop()
			continue

		# Otherwise, add neighbors of newest node to next_neighbors
		next_neighbors.append(set(graph[path[-1]]))

	return all_paths

def read_file(file):
	graph = defaultdict(lambda: set())
	with open(file, 'r') as data:
		for line in [line.strip() for line in data.readlines()]:
			nodes = line.split('-')
			for i in range(len(nodes) - 1):
				graph[nodes[i]].add(nodes[i+1])
				graph[nodes[i+1]].add(nodes[i])
	return graph

print(part_1("input.txt"))
print(part_2("input.txt"))