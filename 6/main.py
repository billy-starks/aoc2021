from collections import Counter

def part_1(file, days=80):
	numbers = read_file(file)

	# Keep a count at each step of how many lanternfish share the same internal timer
	timer_to_count = Counter(numbers)
	for _ in range(days):
		new_count = Counter()

		# Decrement internal timer for each fish
		for timer in timer_to_count:
			new_count[timer - 1] = timer_to_count[timer]

		# Reset fish with count of -1 to 6, and create a new fish with count of 8 for each reset fish
		resetting_fish = new_count[-1]
		del new_count[-1]
		new_count[6] += resetting_fish
		new_count[8] += resetting_fish
		timer_to_count = new_count

	return(sum(timer_to_count.values()))



def read_file(file):
	with open(file, 'r') as data:
		line = data.read()
	numbers = [int(string) for string in line.split(',')]
	return numbers

print(part_1("./input.txt", days=256))