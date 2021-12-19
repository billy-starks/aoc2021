from functools import reduce
from math import ceil, floor
from time import sleep
import itertools

def read_file(file):
	with open(file, 'r') as data:
		return [parse_to_tree(eval(line)) for line in data.readlines()]

def parse_to_tree(snailfish_num):
	tree = Node(None)
	for item in snailfish_num:
		if type(item) == int:
			tree.add_child(Node(item))
		else:
			tree.add_child(parse_to_tree(item))
	return tree

def add_snailfish(tree1, tree2):
	# Do the basic addition
	tree1 = tree1.copy()
	tree2 = tree2.copy()
	tree = Node(None)
	tree.add_child(tree1)
	tree.add_child(tree2)
	
	# Do reduction
	while True:
		if tree.depth() > 4:
			tree = explode_snailfish(tree)
			continue
		tree, did_split = split_snailfish(tree)
		if did_split:
			continue
		break

	return tree

def explode_snailfish(tree):
	# Navigate to the leftmost subtree with highest depth
	exploding_pair = tree
	while exploding_pair.depth() > 1:
		exploding_pair = (exploding_pair._children[0] if exploding_pair._children[0].depth() >= exploding_pair._children[1].depth() 
						  else exploding_pair._children[1])
	left = exploding_pair._children[0].get_left()
	right = exploding_pair._children[1].get_right()
	if left is not None:
		left._value += exploding_pair._children[0]._value
	if right is not None:
		right._value += exploding_pair._children[1]._value
	exploding_pair.replace_self()
	return tree


def split_snailfish(tree):
	current = tree.get_leftest_child()
	while current is not None:
		if current._value >= 10:
			left_child = floor(current._value / 2)
			right_child = ceil(current._value / 2)
			current.add_child(Node(left_child))
			current.add_child(Node(right_child))
			return tree, True
		current = current.get_right()
	return tree, False

def magnitude_snailfish(tree):
	if len(tree._children) == 0:
		return tree._value
	return (3*magnitude_snailfish(tree._children[0]) + 2*magnitude_snailfish(tree._children[1]))

class Node():
	def __init__(self, value=None):
		self._value = value
		self._children = []
		self._parent = None
		self._parent_index = None

	def __str__(self):
		if len(self._children) == 0:
			return str(self._value)
		return "[" + ",".join(str(child) for child in self._children) + "]"

	def add_child(self, child):
		child._parent = self
		child._parent_index = len(self._children)
		self._children.append(child)

	def depth(self):
		if len(self._children) == 0:
			return 0
		return 1 + max(child.depth() for child in self._children)

	def get_leftest_child(self):
		leftest = self
		while len(leftest._children) > 0:
			leftest = leftest._children[0]
		return leftest

	def get_rightest_child(self):
		rightest = self
		while len(rightest._children) > 0:
			rightest = rightest._children[-1]
		return rightest

	def get_left(self):
		if self._parent == None:
			return None

		if self._parent_index != 0:
			directly_left = self._parent._children[self._parent_index - 1]
			return directly_left.get_rightest_child()

		left_of_parent = self._parent.get_left()
		if not left_of_parent:
			return None
		return left_of_parent.get_rightest_child()

	def get_right(self):
		if self._parent == None:
			return None

		if self._parent_index != len(self._parent._children) - 1:
			directly_right = self._parent._children[self._parent_index + 1]
			return directly_right.get_leftest_child()

		right_of_parent = self._parent.get_right()
		if not right_of_parent:
			return None
		return right_of_parent.get_leftest_child()


	def replace_self(self, value=0):
		self._value = value
		self._children = []

	def copy(self):
		root = Node(self._value)
		if len(self._children) == 0:
			return root
		for child in self._children:
			root.add_child(child.copy())
		return root
			


def part_1(file):
	snailfish_nums = read_file(file)
	snailfish_sum = reduce(add_snailfish, snailfish_nums)
	print(snailfish_sum)
	return magnitude_snailfish(snailfish_sum)

def part_2(file):
	snailfish_nums = read_file(file)
	largest_magnitude = 0
	largest_tree = None
	largest_sns = None
	for sn1, sn2 in itertools.permutations(snailfish_nums, 2):
		sn_sum = add_snailfish(sn1, sn2)
		magnitude = magnitude_snailfish(sn_sum)
		largest_magnitude = max(magnitude, largest_magnitude)
		if magnitude == largest_magnitude:
			largest_tree = sn_sum
			largest_sns = (sn1, sn2)
	return largest_magnitude


print(part_1("input.txt"))
print(part_2("input.txt"))

