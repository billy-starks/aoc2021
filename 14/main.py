from collections import Counter
from math import ceil

def part_1(file):
	start, rules = read_file(file)
	current = do_insert(start, rules, 10)
	counter = Counter(current)
	ordered = counter.most_common()
	return(ordered[0][1] - ordered[-1][1])

def part_2(file):
	start, rules = read_file(file)
	counts = do_insert_2(start, rules, 40)
	char_counts = Counter()

	# Count the individual letters in each pair
	for pair, count in counts.items():
		left, right = pair
		char_counts[left] += count
		char_counts[right] += count

	# Every character except the first is counted twice (as the left and right character of a pair)
	# Dividing by 2 and rounding up gives the actual character count
	for char, count in char_counts.items():
		char_counts[char] = ceil(count / 2)
	ordered = char_counts.most_common()
	return(ordered[0][1] - ordered[-1][1])
	

def do_insert(start, rules, steps):
	steps_complete = 0
	current = start
	while steps_complete < steps:
		inserts = get_inserts(current,rules)
		current = interweave(current, inserts)
		steps_complete += 1
	return current

def get_inserts(current, rules):
	inserts = []
	for i in range(len(current) - 1):
		if current[i:i+2] in rules:
			inserts.append(rules[current[i:i+2]])
	return inserts

def interweave(current, inserts):
	new = current[0]
	index = 0
	for index in range(len(inserts)):
		new += inserts[index]
		new += current[index + 1]
	return new

def do_insert_2(start, rules, steps):
	pair_counts = Counter(f"{start[i]}{start[i+1]}" for i in range(len(start) - 1))
	for _ in range(steps):
		next_pair_counts = Counter()
		for pair, count in pair_counts.items():
			if pair in rules:
				inserted = rules[pair]
				left_pair = pair[0] + inserted
				right_pair = inserted + pair[1]
				next_pair_counts[left_pair] += count
				next_pair_counts[right_pair] += count
		pair_counts = next_pair_counts
	return pair_counts

def read_file(file):
	rules = {}
	with open(file, 'r') as data:
		lines = data.readlines()
	start = lines[0].strip()
	for line in lines[2:]:
		pair, insertion = line.strip().split('->')
		pair = pair.strip(); insertion = insertion.strip()
		rules[pair] = insertion
	return start, rules

print(part_1("input.txt"))
print(part_2("input.txt"))