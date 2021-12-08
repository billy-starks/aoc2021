from collections import defaultdict
from pprint import pprint
import random

def part_1(file):
	count = 0
	for in_signals, out_signals in zip(*read_file(file)):
		count += sum([len(signals) for signals in get_unique_segments(out_signals).values()])
	return count

def part_2(file):
	count = 0
	for in_signals, out_signals in zip(*read_file(file)):
		number_to_signals = get_unique_segments(in_signals)
		number_to_signals.update(get_unique_segments(out_signals))
		number_to_signal = {number: set(signals[0]) for number, signals in number_to_signals.items()}

		# Use set difference of numbers with unique signals to identify pairs of segment signals
		a_segment_signal = number_to_signal[7] - number_to_signal[1]
		b_and_d_segment_signal = number_to_signal[4] - number_to_signal[1]
		e_and_g_segment_signal = number_to_signal[8] - number_to_signal[4] - a_segment_signal
		c_and_f_segment_signal = number_to_signal[8] - b_and_d_segment_signal - e_and_g_segment_signal - a_segment_signal

		input_segments = get_all_segments(in_signals)

		# To identiy e and g segment, note that 4 numbers contain e, and six contain g
		e_segment_signal, g_segment_signal = split_signal_pair(e_and_g_segment_signal, input_segments, count=4)

		# For b and d, b appears 6 times, and d appears 7 times
		b_segment_signal, d_segment_signal = split_signal_pair(b_and_d_segment_signal, input_segments, count=6)

		# For c and f, c appears 8 times, and f appears 9 times
		c_segment_signal, f_segment_signal = split_signal_pair(c_and_f_segment_signal, input_segments, count=8)

		# Now we know all 7 segments, can construct the rest of the numbers
		number_to_signal[0] = a_segment_signal | b_segment_signal | c_and_f_segment_signal | e_and_g_segment_signal
		number_to_signal[2] = a_segment_signal | c_segment_signal | d_segment_signal | e_and_g_segment_signal
		number_to_signal[3] = a_segment_signal | c_and_f_segment_signal | d_segment_signal | g_segment_signal
		number_to_signal[5] = a_segment_signal | b_and_d_segment_signal | f_segment_signal | g_segment_signal
		number_to_signal[6] = a_segment_signal | b_and_d_segment_signal | e_and_g_segment_signal | f_segment_signal
		number_to_signal[9] = a_segment_signal | b_and_d_segment_signal | c_and_f_segment_signal | g_segment_signal

		# Convert to hashable reverse map
		signal_to_number = {"".join(sorted(value)): str(key) for key,value in number_to_signal.items()}
		
		output_num = ""
		for signal in out_signals:
			output_num += signal_to_number["".join(sorted(signal))]
		count += int(output_num)
	return count

def split_signal_pair(segment_pair, input_segments, count):
	some_signal = list(segment_pair)[0]
	some_count = len([segment for segment in input_segments if some_signal in segment])
	first_segment_signal = set(some_signal) if some_count == count else (segment_pair - set(some_signal))
	second_segment_signal = segment_pair - first_segment_signal
	return first_segment_signal, second_segment_signal

def read_file(file):
	inputs = []
	outputs = []
	with open(file, 'r') as data:
		for line in data:
			in_signals, out_signals = line.split("|")
			in_signals = in_signals.split()
			out_signals = out_signals.split()
			inputs.append(in_signals)
			outputs.append(out_signals)
	return inputs, outputs

def get_unique_segments(signals):
	number_to_signals = defaultdict(lambda: [])
	for signal in signals:
		if len(signal) == 2:
			number_to_signals[1].append(signal)
		if len(signal) == 4:
			number_to_signals[4].append(signal)
		if len(signal) == 3:
			number_to_signals[7].append(signal)
		if len(signal) == 7:
			number_to_signals[8].append(signal)
	return number_to_signals

def get_all_segments(signals):
	return [set(signal) for signal  in signals]

print(part_1("input.txt"))
print(part_2("input.txt"))