import random
from database import DBHelper
import itertools
import gayme

card_stack_ugly = [
    'Ac', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', 'Jc', 'Qc',
    'Kc', 'As', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'Js',
    'Qs', 'Ks', 'Ah', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h',
    'Jh', 'Qh', 'Kh', 'Ad', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d',
    '10d', 'Jd', 'Qd', 'Kd'
]

card_stack = [
    'A♣', '2♣','3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣',
    'K♣', 'A♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠',
    'Q♠', 'K♠', 'A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥',
    'J♥', 'Q♥', 'K♥', 'A♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦',
    '10♦', 'J♦', 'Q♦', 'K♦'
]


# 0 = not ready, 1 = ready, 2 = bet, 3 = check, 4 = raise, 5 = fold
"""
test_room_list = {"124123 (roomID)": {
  "pot": 100,
  "no_of_players": 2,

  "starting_position": 0,
  "owner": 131231
  "position": ["1235123 (chatid1)", "5412321(chatid2)"],
  "state_of_game": "not_started/started/pre_flop/flop/turn/river/end_of_game ( 1 is game started, 0 is game not started",
  "state_of_cards": ["1c", "5c", "2h"], #All cards that are not out yet
  "players": {
        "1235123 (chatid1)": {
          "cards": []
          "state": 1
          
        }
        "5412321 (chatid2)": {
          "cards": []
          "state" 0
        } 
      }},
  "451233 (roomID)":{
      "pot": 100,
  "no_of_players": 2,
  "starting_position": 0,
  "position": ["1235123 (chatid1)", "5412321(chatid2)"],
  "state_of_game": "1/0 ( 1 is game started, 0 is game not started",
  "state_of_cards": ["1c", "5c", "2h"], #All cards that are not out yet
  "players": {
        "1235123 (chatid1)": {"state" : 0,
        "cards": ["3s, 2h"], #card they have 
        "balance": 0}, # balance (retrieve from db when first game start)
        "5412321 (chatid2)": "8c, 5d" 
      }}}
"""
db = DBHelper()
room_list = {}


def check_if_user_in_room(chatID):
	player_in_room = db.get_users(chatID, "roomID")
	# If user is not in a room
	if player_in_room == [("", )]:
		return False
	else:
		#return player_in_room
		return True


def check_if_player_is_owner(chatID, roomID):
	if room_list[roomID]['owner'] == chatID:
		return True
	return False


def check_players_ready(chatID, roomID):
	if check_if_user_in_room(chatID) is True:
		if roomID in room_list.keys():
			players_not_ready = []
			for key, value in room_list[roomID]['players'].items():
				if value['state'] == 0:
					players_not_ready.append(key)
			if len(players_not_ready) == 0:
				return True
			return players_not_ready


def create_room(chatID):
	if check_if_user_in_room(chatID) is False:
		#check if room creater has sufficient balance
		if (check_sufficient_balance(chatID) is False):
			return "bal"
		# generated_num = 111111

		generated_num = str(random.randint(100000, 900000))
		if generated_num in room_list.keys():
			create_room(chatID)
		else:
			room_list[generated_num] = {
			    "pot": 0,
			    "owner": chatID,
			    "cards_on_table": [],
			    "no_of_players": 1,
			    "position": [chatID],
			    "state_of_game": "not_started",
			    "state_of_cards": [],  #All cards that are not out yet
			    "players": {
			        chatID: {
			        		"nickname": retrieve_players_nickname(chatID),
			            "state": 0,
			            "cards": [],
			            "balance": retrieve_players_balance(chatID),
			            "pre_flop": 0,
			            "flop": 0,
			            "turn": 0,
			            "river": 0
			        }
			    }
			}
			db.edit_users(chatID, "roomID", generated_num)
		return generated_num
	else:
		return False


def join_room(roomID, chatID):
	if check_if_user_in_room(chatID) is False:
		# check if room exists
		if roomID in room_list.keys():
			# check if game has started, if not started, can join
			# check if every player has atleast $20
			if (check_sufficient_balance(chatID) is False):
				return "bal"

			if room_list[roomID]["no_of_players"] <= 9:
				if room_list[roomID]['state_of_game'] == "not_started":
					individual_room = room_list[roomID]
					individual_room["no_of_players"] += 1
					individual_room['position'].append(chatID)
					individual_room['players'][chatID] = {
							"nickname": retrieve_players_nickname(chatID),
					    "state": 0,
					    "cards": [],
					    "balance": retrieve_players_balance(chatID),
					    "pre_flop": 0,
					    "flop": 0,
					    "turn": 0,
					    "river": 0
					}  #cards number
					db.edit_users(chatID, "roomID", roomID)
					return True
	return False


def balance_transaction(chatID, roomID, amount, action):
	if action == "add":
		room_list[roomID]["players"][chatID]["balance"] += amount
	elif action == "subtract":
		room_list[roomID]["players"][chatID]["balance"] -= amount
		return True
	else:
		return False
		
		
def get_room(roomID):
	room = room_list[roomID]
	return room
	
def update_room(roomID, room):
	try:
		room['state_of_game'] = room_list[roomID]['state_of_game']
		room_list[roomID] = room
		
		return True
	except:
		return False
	
def transaction(chatID, roomID, amount, round):
	balance = room_list[roomID]["players"][chatID]["balance"]
	round_balance = room_list[roomID]['players'][chatID][round]
	if (round_balance == amount):
		return True
	else:
		diff = amount - round_balance
		if balance >= 0 and balance >= diff:
			balance -= diff
			room_list[roomID]['players'][chatID][round] = diff
			room_list[roomID]["players"][chatID]["balance"] = balance
			return True
		else:
			return False


def check_sufficient_balance(chatID):
	#return true if player has the min bal
	min_bal = 20
	try:
		balance = retrieve_players_balance(chatID)
		if (balance != False and balance >= min_bal):
			return True
		return False
	except:
		return False


def retrieve_players_nickname(chatID):
	#update player balance for room from DB - call at start of new game/new person join
	try:
		nickname = db.get_users(chatID, "nickname")[0][0]
		return nickname
	except:
		return False

def retrieve_players_balance(chatID):
	#update player balance for room from DB - call at start of new game/new person join
	try:
		balance = db.get_users(chatID, "balance")[0][0]
		return balance
	except:
		return False


def update_players_balance(chatID, roomID):
	#update player balance for DB from room - call this everytime someone leave room/new person join
	try:
		balance = room_list[roomID]["players"][chatID]["balance"]
		db.edit_users(chatID, "balance", balance)
		return True
	except:
		return False

def get_ready(chatID, roomID):
	if check_if_user_in_room(chatID) is True:
		# check if room exists
		if roomID in room_list.keys():
			if room_list[roomID]['state_of_game'] == "not_started":
				if room_list[roomID]['players'][chatID]["state"] == 0:
					room_list[roomID]['players'][chatID]["state"] = 1
					return True
	return False

def check_round(roomID):
	return room_list[roomID]['state_of_game']

def next_round(roomID):
	"""
	Advances room to next round
	Input: roomID
	Output: NIL
	"""
	round_list = ['not_started', "started", "pre_flop", "flop", "turn", "river", "end_of_game"]
	current_round_index = round_list.index(room_list[roomID]['state_of_game'])
	if current_round_index == 6:
		room_list[roomID]['state_of_game'] = round_list[0]
	else:
		room_list[roomID]['state_of_game'] = round_list[current_round_index + 1]
	if current_round_index == 2:
		#pop 3 cards send to cards on middle
		cards_drawn = draw_card(roomID, 3)
		room_list[roomID]['cards_on_table'].extend(cards_drawn)
	elif current_round_index == 3:
		#pop 1 card send to the middle
		cards_drawn = draw_card(roomID, 1)
		room_list[roomID]['cards_on_table'].extend(cards_drawn)
	elif current_round_index == 4:
		#pop 1 card send to the middle
		cards_drawn = draw_card(roomID, 1)
		room_list[roomID]['cards_on_table'].extend(cards_drawn)
	return room_list[roomID]['cards_on_table']
	
def start_game(chatID, roomID):  #Need to add in additional stuff but not really sure what yet
	"""
  Check if more than 2 players
  Need to change the state of the game to 1
  Draw cards for each players based on starting position
  Shuffle cards
  """
	if room_list[roomID]['state_of_game'] == "not_started":
		if room_list[roomID]['no_of_players'] >= 2:
			ready_check = check_players_ready(chatID, roomID)
			if ready_check is True:
				room_list[roomID]['state_of_game'] = "pre_flop"
				game_cards = shuffle_card(card_stack)
				room_list[roomID]['state_of_cards'] = game_cards
				for x in range(2):
					for i in room_list[roomID]['position']:
						cards_drawn = draw_card(roomID, 1)
						room_list[roomID]['players'][i]['cards'].append(cards_drawn[0])
				individual_room = room_list[roomID]
				return individual_room
			return ready_check
	else:
		return False
		
def find_index(leest, item):
	"""
	Find the item's index from a list provided and return to function caller
	
	"""
	return leest.index(item)

def kick_players(chatID, kickPlayerID, roomID):
	roomID = db.get_users(chatID, roomID)
	if roomID == [("", )]:
		return "Player not in room"
	else:
		roomID = roomID[0][0]
		if room_list[roomID]['state_of_game'] == "started":
			return "Player in game"
		else:
			if (update_players_balance(chatID)):
				pass
			else:
				return False
			del room_list[roomID]["players"][chatID]
			room_list[roomID]["position"].remove(chatID)
			no_of_players = room_list[roomID]["no_of_players"]
			no_of_players -= 1
			db.edit_users(kickPlayerID, "roomID", "")
			return True


def leave_game(chatID):  #Should be working properly
	roomID = db.get_users(chatID, "roomID")
	if roomID == [("", )]:
		return "Player not in room"
	else:
		roomID = roomID[0][0]
		if room_list[roomID]['state_of_game'] == "started":
			return "Player in game"
		else:
			#update player balance back into db before leaving
			if (update_players_balance(chatID, roomID)):
				pass
			else:
				return False
			del room_list[roomID]["players"][chatID]
			room_list[roomID]["position"].remove(chatID)
			no_of_players = room_list[roomID]["no_of_players"]
			no_of_players -= 1
			db.edit_users(chatID, "roomID", "")
			if no_of_players <= 0:
				del room_list[roomID]
				return "Deleted Room"
			return True


def reset_game(roomID):
	room_list[roomID]['pot'] = 0
	room_list[roomID]['state_of_game'] = "not_started"
	room_list[roomID]['state_of_cards'] = shuffle_card(card_stack)
	return


def draw_card(roomID, number_of_cards):
	"""
  UPDATE database/dict
  draw card by sequence right?

  """
	card_stack = []
	individual_room = room_list[roomID]
	card_stack_of_room = room_list[roomID]['state_of_cards']
	for i in range(number_of_cards):
		card_stack.append(card_stack_of_room.pop())
	room_list[roomID]['state_of_cards'] = card_stack_of_room 
	return card_stack
	
#	position = individual_room["position"]
#	players = individual_room["players"]
#	for i in range(number_of_cards):
#		for player in position:
#			card = card_stack.pop()
#			players[player]['cards'].append(card)
#	return card_stack


def shuffle_card(card_stack):
	temp_card_stack = card_stack
	random.shuffle(temp_card_stack)
	return temp_card_stack


def check_cards():
  pass

def end_round(roomID):
	#results
  #{'123456': [(('8d', 'Qc', '6c', '7h', '10d'), 1402536)], '654321': [(('5d', '3c', '4d', '6c', '7h'), 3796882)]}
  
  #pots
   #pots_list = {'pot_1': {'amount': 3060, 'players': [1, 2, 3, 4, 5, 6, 7, 8, 9]}, 'pot_2': {'amount': 800, 'players': [1, 2, 3, 5, 6, 7, 8, 9]}, 'pot_3': {'amount': 2100, 'players': [1, 3, 5, 6, 7, 8, 9]}, 'pot_4': {'amount': 900, 'players': [1, 3, 6, 7, 8, 9]}, 'pot_5': {'amount': 250, 'players': [1, 3, 7, 8, 9]}, 'pot_6': {'amount': 400, 'players': [1, 3, 7, 8]}, 'pot_7': {'amount': 1050, 'players': [3, 7, 8]}, 'pot_8': {'amount': 300, 'players': [3, 7]}}
  
  # get all the variables
	ljb = gayme.LanJiaoBin()
	table = room_list[roomID]['cards_on_table']
	player_cards = {}
	winnings = {}
	for player in room_list[roomID]['players']:
		player_cards[str(player)] = []
		player_cards[str(player)].extend(room_list[roomID]['players'][player]['cards'])

	pots_list = creating_pot(roomID)	
	results = ljb.determine_scores_dict(player_cards, table)
	
	#associating winnings to player
	total_winnings = []
	for x in pots_list:
		players = pots_list[x]['players']
		points = []
		winners = []
		winnings = []
		for player in players:
			points.append(results[str(player)][0][1])
			
		highest=max(points)
		for player in players:
			if results[str(player)][0][1] == highest:
				winners.append(player)
		
		if len(winners) > 1:
			for winner in winners:
				if winner in pots_list[x]['players']:
					winnings.append(winner)
			winnings.append(pots_list[x]['amount'])
			
		else:
			if winners[0] in pots_list[x]['players']:
				winnings.append(winners[0])
				winnings.append(pots_list[x]['amount'])
		
		total_winnings.append(winnings)
	return total_winnings
	
def creating_pot(roomID):
  players = room_list[roomID]["players"]
  pots = {"pre_flop": {},
          "flop": {},
          "turn": {},
          "river": {}
  }
  players_left = [i for i in room_list[roomID]["players"].keys()]
  no_of_players = room_list[roomID]["no_of_players"] 
  for key, value in players.items():
    pots['pre_flop'][value['pre_flop']] = []
    pots['flop'][value['flop']] = []
    pots['turn'][value['turn']] = []
    pots['river'][value['river']] = []
  for key, value in players.items():
    pots['pre_flop'][value['pre_flop']].append(key)
    pots['flop'][value['flop']].append(key)
    pots['turn'][value['turn']].append(key)
    pots['river'][value['river']].append(key)
  if 0 in list(pots['pre_flop'].keys()):
    del pots['pre_flop'][0]
  if 0 in list(pots['flop'].keys()):
    del pots['flop'][0]
  if 0 in list(pots['turn'].keys()):
    del pots['turn'][0]
  if 0 in list(pots['river'].keys()):
    del pots['river'][0]
    
  #pre_flop
  if len(set(pots['pre_flop'].keys())) == 1:
    pots["pot_1"] = {}
    pre_flop = list(pots['pre_flop'].keys())[0]
    pots["pot_1"]["amount"] =  pre_flop * no_of_players
    pots["pot_1"]["players"] = [x for x in players_left]
  else:
    unique_list = list(k for k,_ in itertools.groupby(sorted(pots['pre_flop'].keys())))
    for x in range(len(set(pots['pre_flop'].keys()))):
      pots["pot_{}".format(x+1)] = {}
      if x == 0:
        pots["pot_{}".format(x+1)]["amount"] = unique_list[x] * (no_of_players)
        pots["pot_{}".format(x+1)]["players"] = [x for x in players_left]
        for x in  pots['pre_flop'][unique_list[x]]:
          players_left.remove(x)
      else:
        pots["pot_{}".format(x+1)]["amount"] = (unique_list[x] - unique_list[x-1]) * len(players_left)
        pots["pot_{}".format(x+1)]["players"] = [x for x in players_left]
        if len(set(pots['pre_flop'].keys())) != x - 1:
          for x in pots['pre_flop'][unique_list[x]]:
            players_left.remove(x)
          
  #FLOP
  last_pot = list(pots.keys())[-1].replace("pot_", "")
  if len(set(pots['flop'].keys())) == 1:
    flop = list(pots['flop'].keys())[0]
    pots["pot_{}".format(str(last_pot))]['amount'] = pots['pot_{}'.format(last_pot)]['amount'] + (flop * len(players_left))
  else:
    unique_list = list(k for k,_ in itertools.groupby(sorted(pots['flop'].keys())))
    
    for x in range(len(set(pots['flop'].keys()))):
      if x == 0:
        pots["pot_{}".format(str(last_pot))]['amount'] += (unique_list[x] * len(players_left))
        pots["pot_{}".format(str(last_pot))]["players"] = [x for x in players_left]
        if len(set(pots['flop'].keys())) != x + 1:
          for x in  pots['flop'][unique_list[x]]:
            players_left.remove(x)
      else:
        pots["pot_{}".format(str(int(last_pot) + x))] = {}
        pots["pot_{}".format(str(int(last_pot) + x))]["amount"] = (unique_list[x] - unique_list[x-1]) * len(players_left)
        pots["pot_{}".format(str(int(last_pot) + x))]["players"] = [x for x in players_left]
        if len(set(pots['flop'].keys())) != x + 1:
          for x in pots['flop'][unique_list[x]]:  
            players_left.remove(x)

  #TURN
  last_pot = list(pots.keys())[-1].replace("pot_", "")
  if len(set(pots['turn'].keys())) == 1:
    turn = list(pots['turn'].keys())[0]
    if len(players_left) == len(pots["pot_{}".format(str(last_pot))]["players"]):
      pots["pot_{}".format(str(last_pot))]['amount'] = pots['pot_{}'.format(last_pot)]['amount'] + (turn * len(players_left))
    else:
      pots["pot_{}".format(str(int(last_pot)+1))] = {}
      pots["pot_{}".format(str(int(last_pot)+1))]['amount'] = turn * len(players_left)
  else:
    unique_list = list(k for k,_ in itertools.groupby(sorted(pots['turn'].keys())))
    for x in range(len(set(pots['turn'].keys()))):
      if x == 0:
        pots["pot_{}".format(str(last_pot))]['amount'] += (unique_list[x] * len(players_left))
        pots["pot_{}".format(str(last_pot))]["players"] = [x for x in players_left]
        if len(set(pots['turn'].keys())) != x + 1:
          for x in  pots['turn'][unique_list[x]]:
            players_left.remove(x)
      else:
        pots["pot_{}".format(str(int(last_pot) + x))] = {}
        pots["pot_{}".format(str(int(last_pot) + x))]["amount"] = (unique_list[x] - unique_list[x-1]) * len(players_left)
        pots["pot_{}".format(str(int(last_pot) + x))]["players"] = [x for x in players_left]
        if len(set(pots['turn'].keys())) != x + 1:
          for x in pots['turn'][unique_list[x]]:
            players_left.remove(x)
  
  #RIVER
  last_pot = list(pots.keys())[-1].replace("pot_", "")
  if len(set(pots['river'].keys())) == 1:
    river = list(pots['river'].keys())[0]
    if len(players_left) == len(pots["pot_{}".format(str(last_pot))]["players"]):
      pots["pot_{}".format(str(last_pot))]['amount'] = pots['pot_{}'.format(last_pot)]['amount'] + (river * len(players_left))
    else:
      pots["pot_{}".format(str(int(last_pot)+1))] = {}
      pots["pot_{}".format(str(int(last_pot)+1))]['amount'] = river * len(players_left)
      
  else:
    unique_list = list(k for k,_ in itertools.groupby(sorted(pots['river'].keys())))
    for x in range(len(set(pots['river'].keys()))):
      if x == 0:
        pots["pot_{}".format(str(last_pot))]['amount'] += (unique_list[x] * len(players_left))
        pots["pot_{}".format(str(last_pot))]["players"] = [x for x in players_left]
        if len(set(pots['river'].keys())) != x + 1:
          for x in  pots['river'][unique_list[x]]:
            players_left.remove(x)
      else:
        pots["pot_{}".format(str(int(last_pot) + x))] = {}
        pots["pot_{}".format(str(int(last_pot) + x))]["amount"] = (unique_list[x] - unique_list[x-1]) * len(players_left)
        pots["pot_{}".format(str(int(last_pot) + x))]["players"] = [x for x in players_left]
        if len(set(pots['river'].keys())) != x + 1:
          for x in pots['river'][unique_list[x]]:
            players_left.remove(x)
  
  del pots['pre_flop']
  del pots['flop']
  del pots['turn']
  del pots['river']
  return pots

def main():
  db.setup()
	  
if __name__ == "__main__":
  main()


