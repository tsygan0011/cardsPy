import numpy as np
import random


# Make a deck
def make_decks(num_decks, card_types):
    new_deck = []
    for i in range(num_decks):
        for j in range(4):
            new_deck.extend(card_types)
    random.shuffle(new_deck)
    return new_deck
    
def get_ace_values(temp_list):
    sum_array = np.zeros((2**len(temp_list), len(temp_list)))
    # gets the permutations
    for i in range(len(temp_list)):
        n = len(temp_list) - i
        half_len = int(2**n * 0.5)
        for rep in range(int(sum_array.shape[0]/half_len/2)):
            sum_array[rep*2**n : rep*2**n+half_len, i]=1
            sum_array[rep*2**n+half_len : rep*2**n+half_len*2, i]=11
    # return values that are valid (<=21)
    return list(set([int(s) for s in np.sum(sum_array, axis=1)\
                     if s<=21]))
                     
def ace_values(num_aces):
    temp_list = []
    for i in range(num_aces):
        temp_list.append([1,10])
    return get_ace_values(temp_list)
    
    
    
def total_up(hand):
    aces = 0
    total = 0
    
    for card in hand:
        if card != 'A':
            total += card
        else:
            aces += 1
    
    # Call function ace_values to produce list of possible values
    # for aces in hand
    ace_value_list = ace_values(aces)
    final_totals = [i+total for i in ace_value_list if i+total<=21]
    # print(f' final {final_totals} ')
    # print(max(final_totals))
    # print(min(ace_value_list))
    
    if final_totals == []:
      return min(ace_value_list) + total
    else:
      return max(final_totals)
        
def main():
  stacks = 50000
  players = 4
  num_decks = 1
  card_types = ['A',2,3,4,5,6,7,8,9,10,10,10,10]
  for stack in range(stacks):
    blackjack1 = set(['A',10])
    blackjack2 = list(['A' , 'A'])
    dealer_cards = make_decks(num_decks, card_types)
    
    while len(dealer_cards) > 20:
        
        curr_player_results = np.zeros((1,players))
        
        dealer_hand = []
        player_hands = [[] for player in range(players)]
        # Deal FIRST card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        dealer_hand.append(dealer_cards.pop(0))
        # Deal SECOND card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        dealer_hand.append(dealer_cards.pop(0))
  
  # Dealer checks for 21
  if set(dealer_hand) == blackjack1 or set(dealer_hand) == blackjack2:
    print("Blackjack!")
    for player in range(players):
        if set(player_hands[player]) != blackjack1 or set(player_hands[player])!= blackjack2:
            curr_player_results[0,player] = -1
            print("dealer 21 player lose")
        else:
            curr_player_results[0,player] = 0
            print("dealer 21 player 21")

  else:
    for player in range(players):
      # Players check for 21
      if set(player_hands[player]) == blackjack1 or set(player_hands[player]) == blackjack2:
        print("dealer nt 21, player 21")
        curr_player_results[0,player] = 1
      else:
        while (total_up(player_hands[player]) <= 17):
          number_of_hands = len(player_hands[player])
          if number_of_hands < 6:
            print("DRAW U FA")
            player_hands[player].append(dealer_cards.pop(0))
            if total_up(player_hands[player]) > 21:
              print("Dealer not 21, player > 21")
              curr_player_results[0,player] = -1
            
          else:
            break
  # Dealer hits based on the rules
  while total_up(dealer_hand) < 17:
    print("DEALER DRAW")  
    dealer_hand.append(dealer_cards.pop(0))
  # Compare dealer hand to players hand 
  # but first check if dealer busted
  if total_up(dealer_hand) > 21:
      for player in range(players):
          if curr_player_results[0,player] != -1:
            print("dealer > 21, player < 21")
            curr_player_results[0,player] = 1
  else:
    for player in range(players):
        if total_up(player_hands[player]) > total_up(dealer_hand):
            if total_up(player_hands[player]) <= 21:
              print("Dealer lose to player")
              curr_player_results[0,player] = 1
        elif total_up(player_hands[player]) == total_up(dealer_hand):
          print("tie")  
          curr_player_results[0,player] = 0
        elif total_up(player_hands[player]) > 21 and total_up(dealer_hand) > 21:
          print("Both busted")
          curr_player_results[0,player] = 0
        else:
          print("dealer wins")  
          curr_player_results[0,player] = -1
            
  print(f' Status of players {curr_player_results} ')
  print(f' Dealer hands {dealer_hand}')
  print(f'{total_up(dealer_hand)} score')
  for i in player_hands:
    print(f'player{i} hands')
    print(f'{total_up(i)} score')
if __name__ == '__main__':
  main()