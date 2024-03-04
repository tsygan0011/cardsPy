#!/usr/bin/python
# -*- coding: utf-8 -*-
from itertools import combinations
import enum

#HAND_RANK = 15**5
HAND_RANK = 15**5

class PokerHands(enum.Enum):

	# It consists of Ten, Jack, Queen, King, and Ace, all of the same suit

	ROYAL_FLUSH = 10

	# It is composed of five consecutive cards of the same suit.
	# If two players have a straight flush, the one with the highest cards wins.

	STRAIGHT_FLUSH = 9

	# 4 cards of the same rank
	# one with the highest rank will win
	# If two players have FOUR_OF_A_KIND, last card higher points wins

	FOUR_OF_A_KIND = 8

	# three-of-a-kind and a pair
	# If two players have a full house, then the one with the highest three-of-a-kind wins
	# If they have the same one, then the pair counts.

	FULL_HOUSE = 7

	# Five cards of the same suit make a flush.
	# If two players have a flush, then the one with the highest cards wins.

	FLUSH = 6

	STRAIGHTS = 5
	THREE_OF_A_KIND = 4
	TWO_PAIR = 3
	PAIR = 2
	HIGH_CARD = 1


# spade > heart>club>diamonds


class LanJiaoBin:

	player_hands = []
	cards = []

	@staticmethod
	def card_rank_to_values(card):

		# Used to convert ranks to intergers like J = 10, Q = 11

		if card[0] == 'J':
			return 11
		if card[0] == 'Q':
			return 12
		if card[0] == 'K':
			return 13
		if card[0] == 'A':
			return 14
		return int(card[:-1])

	def strip_suits(self, hand):

		# Returns a list of the values of the cards without its strip_suits [8C, KD] to [8, 13]

		card_value_list = []
		for card in hand:
			card_value_list.append(self.card_rank_to_values(card))
		return card_value_list

	def strip_ranks(self, hand):
		card_value_list = []
		for card in hand:
			card_value_list.append(card[-1:])
		return card_value_list

	def group_hand(self, hand_values):
		"""
    Function that accepts a list of card values and outputs the how many each value the list contains
    Input: [2,3,2,10,13]
    Output: hand_keys = ['3','10','13','2']
            hand_values = [1,1,1,2]
    """

		dict_hand = {}
		for i in hand_values:
			if i not in dict_hand:
				dict_hand[i] = 0
			dict_hand[i] += 1

		sorted_dict_items = sorted(dict_hand.items(), key=lambda x: \
                                   x[1])

		hand_values = list(map(lambda x: x[1], sorted_dict_items))
		hand_keys = list(map(lambda x: x[0], sorted_dict_items))
		return (hand_values, hand_keys)

	@staticmethod
	def calculate_hand_score(hand_value, poker_hand_type):
		"""
    Calculate hand score by giving value of hand and any hands like royal FLUSH
    Input: 
    """

		score = HAND_RANK * poker_hand_type
		i = 1
		for val in hand_value:
			score += val * i
			i *= 15
		return score
	def get_poker_hand_type(self, hand):
		# Get the card values of users hand and sort them

		hand_values = sorted(self.strip_suits(hand))

		# Check to see if user's had only has a single suit, useful for royal flush

		is_single_suit = len(set(self.strip_ranks(hand))) == 1

		# Group user cards of the same value together

		(grouped_values, grouped_keys) = self.group_hand(hand_values)

		# Check the difference in value between the lowest and highest value

		delta_pos = hand_values[-1] - hand_values[0]

		# Check if the cards are in sequence, useful for flush

		is_in_sequence = delta_pos == 4 and len(grouped_values) == 5

		# Check for royal flush

		if len(grouped_keys) == 5 and hand_values[0] == 10 \
            and is_single_suit:
			return self.calculate_hand_score([], 10)

		# Check for straight flush

		elif is_single_suit and is_in_sequence:
			return self.calculate_hand_score([hand_values[-1]], 9)

		# Check for four of a kind

		if grouped_values == [1, 4]:
			return self.calculate_hand_score(grouped_keys, 8)
		elif grouped_values == [2, 3]:

			# Check for full house

			return self.calculate_hand_score(grouped_keys, 7)
		elif is_single_suit:

			# Check for flush

			return self.calculate_hand_score([hand_values[-1]], 6)
		elif is_in_sequence:

			# Check for straights

			return self.calculate_hand_score([hand_values[-1]], 5)
		elif grouped_values == [1, 1, 3]:

			# Check for three of a kind

			return self.calculate_hand_score(grouped_keys, 4)
		elif grouped_values == [1, 2, 2]:

			# Check for two pair

			return self.calculate_hand_score(grouped_keys, 3)
		elif grouped_values == [1, 1, 1, 2]:

			# Check for pair

			return self.calculate_hand_score(grouped_keys, 2)
		else:

			# Check for high card

			return self.calculate_hand_score(hand_values, 1)

	def best_hand_score(self, hands):
		best_point = 0
		best_hand = []
		for hand in hands:
			hand_point = self.get_poker_hand_type(hand)
			if hand_point > best_point:
				best_hand = hand
				best_point = hand_point
		return (best_hand, best_point)

	@staticmethod
	def generate_combinations(cards):
		possible_hands = combinations(cards, 5)
		return possible_hands

	def determine_scores(self, players, cards_table):
		res = {}
		for player_hand in players:
			player_hands = self.generate_combinations(player_hand + cards_table)
			best_hand, score = self.best_hand_score(player_hands)
			if score not in res:
				res[score] = []
				res[score].append((best_hand, score))
		return res


	def determine_scores_dict(self, players, cards_table):
		res = {}
		for player in players:
			player_hands = self.generate_combinations(players[player] + cards_table)
			best_hand, score = self.best_hand_score(player_hands)
			if score not in res:
				res[player] = []
				res[player].append((best_hand, score))
		return res
		

# ljb = LanJiaoBin()
# hands1 = {"123456": ["8d", "Qc"], "654321": ['2c','5d']}
# table = ['3c', '4d', '6c', '7h', '10d']
# player_cards = {}
# for player in room_list[123123]['players']:
# 		# player = str(player)
# 		print(player)
# 		player_cards[int(player)] = room_list[]player['cards']
# 		print(player_cards)
# print(ljb.determinate_scores_dict(hands1,table))
# print(ljb.determinate_scores(hands,table))
# Players hand: 4C AH
# 'Ad', 'Kd', 'Jd', 'Qd', '10d'
# results = {1: [(('8d', 'Qc', '6c', '7h', '10d'), 1402536)], 2: [(('5d', '3c', '4d', '6c', '7h'), 3796882)]}
# players = [1,2]
# pots_list = {'pot_1': {'amount': 3060, 'players': [1,2]}, 'pot_2': {'amount': 800, 'players': [1, 2]}, 'pot_3': {'amount': 2100, 'players': [1]}}

# expected => [[3060, 2], [800, 2], [2100, 1]]


# total_winnings = []
# for x in pots_list:
# 	players = pots_list[x]['players']
# 	points = []
# 	winners = []
# 	winnings = []
# 	for player in players:
# 		points.append(results[player][0][1])
		
# 	highest=max(points)
# 	for player in players:
# 		if results[player][0][1] == highest:
# 			winners.append(player)
	
# 	if len(winners) > 1:
# 		for winner in winners:
# 			if winner in pots_list[x]['players']:
# 				winnings.append(winner)
# 		winnings.append(pots_list[x]['amount'])
		
# 	else:
# 		if winners[0] in pots_list[x]['players']:
# 			winnings.append(winners[0])
# 			winnings.append(pots_list[x]['amount'])
	
# 	total_winnings.append(winnings)

	
	
# print(total_winnings)