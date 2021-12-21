from itertools import islice, product
from collections import Counter
from dataclasses import dataclass
from typing import Tuple
from pprint import pprint

TEST_PARAMS = (4,8)
INPUT_PARAMS = (5,10)

def deterministic_die_mod():
	i = 1
	while True:
		yield i
		i = (i + 1) % 10

def wrap(n, fake_mod):
	answer = n
	while answer > fake_mod:
		answer = answer - fake_mod
	return answer

def part_1(p1start, p2start, rolls=3):
	die = deterministic_die_mod()
	roll_count = 0
	p1Pos = p1start
	p2Pos = p2start
	p1Score = 0
	p2Score = 0
	while True:
		p1Pos = wrap(p1Pos + sum(islice(die, rolls)), 10); roll_count += rolls
		p1Score += p1Pos
		if p1Score >= 1000:
			print("Player 1 Wins!")
			return p2Score * roll_count


		p2Pos = wrap(p2Pos + sum(islice(die, rolls)), 10); roll_count += rolls
		p2Score += p2Pos
		if p2Score >= 1000:
			print("Player 2 Wins!")
			return p1Score * roll_count

def part_2(p1start, p2start):
	# Don't even try to simulate this; use a hashmap to count the number of universes where
	# player 1 and 2 have a certain score and position. Then remove incomplete games and count
	# the games that result from the incomplete games' continuation until all games are complete
	games = Counter([GameState((p1start,p2start),(0,0))])
	winners = Counter()
	while len(games) > 0:
		# P1's turn
		advanced_games = Counter()
		while len(games) > 0:
			game, count = games.popitem()
			next_games = game.advance_game(0, count)
			advanced_games.update(next_games)
		games = advanced_games
		
		# Count winners
		for game in list(games.keys()):
			if game.is_complete():
				count = games.pop(game)
				winners[game.winner()] += count

		# P2's turn
		advanced_games = Counter()
		while len(games) > 0:
			game, count = games.popitem()
			next_games = game.advance_game(1, count)
			advanced_games.update(next_games)
		games = advanced_games
		
		# Count winners
		for game in list(games.keys()):
			if game.is_complete():
				count = games.pop(game)
				winners[game.winner()] += count
	print(winners)
	return(max(winners.values()))

@dataclass(eq=True, frozen=True)
class GameState():
	positions: Tuple[int]
	scores: Tuple[int]

	def is_complete(self):
		return any(x >= 21 for x in self.scores)

	def winner(self):
		if self.is_complete():
			return "Player 1" if self.scores[0] > self.scores[1] else "Player 2"
		return None

	# Advance quantum state of game, returning a Counter whose keys are advanced game
	# states and whose values are the number of universe in that state
	def advance_game(self, player_index, count=1):
		advanced_games = Counter()
		for i,j,k in product(range(1,4),range(1,4),range(1,4)):
			advanced_games[self._advanced_game_state(player_index, (i+j+k))] += count
		return advanced_games

	def _advanced_game_state(self, player_index, roll_sum):
		p1Pos, p2Pos = self.positions
		p1Pos = wrap(p1Pos + roll_sum, 10) if player_index == 0 else p1Pos
		p2Pos = wrap(p2Pos + roll_sum, 10) if player_index == 1 else p2Pos
		p1Score, p2Score = self.scores
		p1Score += p1Pos if player_index == 0 else 0
		p2Score += p2Pos if player_index == 1 else 0
		return GameState((p1Pos, p2Pos), (p1Score, p2Score))






print(part_1(*INPUT_PARAMS))
print(part_2(*INPUT_PARAMS))