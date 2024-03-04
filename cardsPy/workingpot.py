import itertools
# room_list = { 123123:{
#                 "pot": 0,
#                 "no_of_players": 9,  #All cards that are not out yet
#                 "players": { 1: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 1000,
#                                       "turn": 0,
#                                       "river": 0
#                                       }, 
#                             2: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 400,
#                                       "turn": 0,
#                                       "river": 0
#                                       },
#                             3: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 1000,
#                                       "turn": 100,
#                                       "river": 400
#                                       },
#                             4: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 300,
#                                       "turn": 0,
#                                       "river": 0
#                                       },
#                             5: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 700,
#                                       "turn": 0,
#                                       "river": 0
#                                       },
#                           6: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 850,
#                                       "turn": 0,
#                                       "river": 0
#                                       },
                                      
#                           7: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 1000,
#                                       "turn": 100,
#                                       "river": 0
#                                       },
                                      
#                           8: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 1000,
#                                       "turn": 100,
#                                       "river": 250
#                                       },
                                      
#                           9: {"state": 0,
#                                       "cards": [],
#                                       "balance":0,
#                                       "pre_flop": 40,
#                                       "flop": 900,
#                                       "turn": 0,
#                                       "river": 0
#                                       }
#                 }
#                                   }}

room_list = {123123: {'pot': 0, 'owner': 187662022, 'cards_on_table': ['Qc', '6c', '10d', '5h', '8h'], 'no_of_players': 2, 'position': [187662022, 373261948], 'state_of_game': 'river', 'state_of_cards': ['9h', '4d', '5d', 'Ks', 'Ah', 'As', '8c', '4h', '10c', '3h', '7c', '6s', 'Qs', 'Jh', '3d', '4c', '3c', 'Qh', '4s', '2d', '9d', '3s', '8d', 'Js', 'Ac', '8s', '9s', '5c', '6h', 'Kh', '5s', 'Jc', 'Kc', '6d', '7h', '10s', '9c', '10h', 'Ad', 'Kd', '2c', 'Qd', '7d'], 'players': {187662022: {'nickname': 'You Xiang', 'state': 1, 'cards': ['2s', '2h'], 'balance': 400, 'pre_flop': 150, 'flop': 150, 'turn': 150, 'river': 150}, 373261948: {'nickname': 'Enoch', 'state': 1, 'cards': ['7s', 'Jd'], 'balance': 400, 'pre_flop': 150, 'flop': 150, 'turn': 150, 'river': 150}}
	
}}


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

  #pre-flop
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
		print(players_left)
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
	print(pots)
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


print(creating_pot(123123))
print()
print(room_list[123123])