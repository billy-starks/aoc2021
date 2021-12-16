import operator
import functools

def read_file(file):
	with open(file, 'r') as data:
		hex_string = data.read()
	message_bytes = bytearray.fromhex(hex_string)
	return message_bytes

def get_bits(message_bytes, start, length):
	# Get bytes that contain bits
	start_byte = start // 8
	end_byte = (start + length) // 8
	the_bytes = message_bytes[start_byte:end_byte+1]
	num_bytes = len(the_bytes)

	# Construct mask to select bits
	mask_start = start % 8
	mask_end = mask_start + length
	mask_string = "".join( ("1" if i in range(mask_start, mask_end) else "0") for i in range(8*num_bytes))
	mask = int(mask_string, base=2)
	shift = len(mask_string) - mask_end

	# Get bits as int
	to_int = int.from_bytes(the_bytes, byteorder='big')
	to_int = to_int & mask
	to_int = (to_int >> shift)
	return to_int

def part_1(file):
	message_bytes = read_file(file)
	message, _, version_number_sum = process_packet(message_bytes)
	return(version_number_sum)

def part_2(file):
	message_bytes = read_file(file)
	message, _, version_number_sum = process_packet(message_bytes)
	return(message)

def process_packet(message_bytes, cur=0, version_number_sum=0):
	cursor = cur
	pack_version = get_bits(message_bytes, cursor, 3); cursor += 3
	pack_type = get_bits(message_bytes, cursor, 3); cursor += 3
	current_version_number_sum = pack_version + version_number_sum

	if pack_type == 4: # Only type 4 is a literal value
		message, cursor = process_literal_value(message_bytes, cursor)
		return message, cursor, current_version_number_sum

	else: # All other pack types are operators
		length_type_id = get_bits(message_bytes, cursor, 1); cursor += 1
		subpackets = []
		if length_type_id == 0:
			pack_length_in_bits = get_bits(message_bytes, cursor, 15); cursor += 15
			subpackets, cursor, current_version_number_sum = process_subpackets_bit_length(message_bytes, cursor, pack_length_in_bits, current_version_number_sum)
		elif length_type_id == 1:
			pack_length_in_subpackets = get_bits(message_bytes, cursor, 11); cursor += 11
			subpackets, cursor, current_version_number_sum = process_subpackets_num_subpackets(message_bytes, cursor, pack_length_in_subpackets, current_version_number_sum)

	return_value = 0
	if pack_type == 0: # Sum value of all subpackets
		return_value = sum(subpackets)
	if pack_type == 1: # Product of all values in subpacket
		return_value = functools.reduce(operator.mul, subpackets)
	if pack_type == 2: # Minimum
		return_value = min(subpackets)
	if pack_type == 3: # Maximum
		return_value = max(subpackets)

	if pack_type == 5: # Return (first value > second value); always two values
		return_value = 1 if subpackets[0] > subpackets[1] else 0
	if pack_type == 6: # Return (first value < second value); always two values
		return_value = 1 if subpackets[0] < subpackets[1] else 0
	if pack_type == 7:
		return_value = 1 if subpackets[0] == subpackets[1] else 0

	return return_value, cursor, current_version_number_sum

def process_literal_value(message_bytes, cursor):
	value = 0
	while True:
		is_more_bit = get_bits(message_bytes, cursor, 1); cursor += 1
		num_bits = get_bits(message_bytes, cursor, 4); cursor += 4
		value = (value * 16) + num_bits
		if not is_more_bit:
			break
	return value, cursor

def process_subpackets_bit_length(message_bytes, cursor, pack_length_in_bits, version_number_sum):
	start = cursor
	subpackets = []
	current_version_number_sum = version_number_sum
	while cursor < (start + pack_length_in_bits):
		message, cursor, current_version_number_sum = process_packet(message_bytes, cursor, current_version_number_sum)
		subpackets.append(message)
	return subpackets, cursor, current_version_number_sum

def process_subpackets_num_subpackets(message_bytes, cursor, pack_length_in_subpackets, version_number_sum):
	subpackets = []
	current_version_number_sum = version_number_sum
	for _ in range(pack_length_in_subpackets):
		message, cursor, current_version_number_sum = process_packet(message_bytes, cursor, current_version_number_sum)
		subpackets.append(message)
	return subpackets, cursor, current_version_number_sum


print(part_1("input.txt"))
print(part_2("input.txt"))
