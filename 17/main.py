from time import sleep
from math import ceil

TEST_PARAMS = [(20, 30), (-10, -5)]
INPUT_PARAMS = [(179, 201), (-109, -63)]
STARTING_POS = (0,0)

def probe_launch_simulation(t, init_pos, init_vel):
	cur_pos = list(init_pos)
	cur_vel = list(init_vel)
	points = []
	for _ in range(t):
		cur_pos[0] += cur_vel[0]
		cur_pos[1] += cur_vel[1]
		cur_vel[0] = (cur_vel[0] - 1) if cur_vel[0] > 0 else (cur_vel[0] + 1) if cur_vel[0] < 0 else 0
		cur_vel[1] = cur_vel[1] - 1
		points.append(tuple(cur_pos))
	return points

def probe_launch_peak_and_target(init_pos, init_vel, target_x_range, target_y_range):
	peak_t = init_vel[1]
	sim_offset = 60
	sim_offset += ceil(abs(target_y_range[1] / peak_t)) if peak_t != 0 else 0
	sim_offset += ceil(abs(target_x_range[1] / init_vel[0])) if init_vel[0] != 0 else 0
	sim_length = max(0, peak_t) * 2
	points = probe_launch_simulation(sim_length + sim_offset, init_pos, init_vel)
	peak_y = points[peak_t][1] if 0 <= peak_t < len(points) else points[0][-1] if peak_t < 0 and len(points) != 0 else -9999999
	return peak_y, any(in_target(point, target_x_range, target_y_range) for point in points)

def get_x_to_check(init_x, target_x_range):
	x = 0
	min_x = 0
	target_x_min, target_x_max = target_x_range
	while x < target_x_min:
		min_x += 1
		x += min_x

	return min_x, target_x_max

def get_y_to_check(init_y, target_y_range):
	target_y_min, target_y_max = target_y_range
	max_y = 0
	if target_y_min < 0 and target_y_max < 0:
		max_y = -target_y_min
	return target_y_min, max_y

def in_target(point, target_x_range, target_y_range):
	min_x, max_x = target_x_range
	min_y, max_y = target_y_range
	return (min_x <= point[0] <= max_x) and (min_y <= point[1] <= max_y)

def part_1(target_x_range, target_y_range):
	peak_y = -9999999
	min_x, max_x = get_x_to_check(0, target_x_range)
	min_y, max_y = get_y_to_check(0, target_y_range)
	for x in range(min_x, max_x+1):
		for y in range(min_y, max_y+1):
			peak, hit_target = probe_launch_peak_and_target(STARTING_POS, (x,y), target_x_range, target_y_range)
			if hit_target:
				peak_y = max(peak, peak_y)
	return peak_y

def part_2(target_x_range, target_y_range):
	min_x, max_x = get_x_to_check(0, target_x_range)
	min_y, max_y = get_y_to_check(0, target_y_range)
	count = 0
	for x in range(min_x, max_x+1):
		for y in range(min_y, max_y+1):
			_, hit_target = probe_launch_peak_and_target(STARTING_POS, (x,y), target_x_range, target_y_range)
			if hit_target:
				count += 1
	return count


print(part_1(*INPUT_PARAMS))
print(part_2(*INPUT_PARAMS))