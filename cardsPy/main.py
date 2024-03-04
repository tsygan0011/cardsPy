from telegram import (ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (CommandHandler, CallbackQueryHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
import random
import server
from database import DBHelper

CHANGE_NICKNAME = range(1)
KICKING = range(1)
ACTION = range(1)

db = DBHelper()

def build_menu(buttons, n_cols, header_buttons = None, footer_buttons = None):
	menu= [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
	if header_buttons:
		menu.insert(0, header_buttons)
	if footer_buttons:
		menu.insert(0, footer_buttons)
	return menu

def start(update, context):
	"""
  A user will start the telegram bot with this. Explain what the bot does and how to use it.
  """
	message = """Greetings my horny KTV uncle! Thanks for your contributions to Phase 2 HA! This is a bot that allows you to play poker with your other horny friends! Don't worry, police won't catch you here haha
	
To create a room, type /create and a number will be generated. Send this number to your friends and they can use /join <NUMBER> to join your room.

What is the nickname you would like to choose? This cannot be changed in the future (until further updates). Just type in your name.
  """
	#
	update.message.reply_text(message)
	return CHANGE_NICKNAME


def change_nickname(update, context):  #might need to change this part
	nickname = update.message.text
	if db.add_users(nickname, update.message.from_user.id):
		message = "Hello {}! Welcome to our poker bot.".format(nickname)
		update.message.reply_text(message)
		return ConversationHandler.END


def create(update, context):
	"""
  Create a host room and return the room number.
  """
	room_number = server.create_room(update.message.from_user.id)
	if type(room_number) is str:
		message = """You have created a room! The room number is <b>{}</b>, you may ask your friends to join by typing /join {}. The minimum players to start will be 2 and the maximum players of a room is 9.""".format(
		    room_number, room_number)
		update.message.reply_text(message, parse_mode=ParseMode.HTML)
	elif room_number is False:
		update.message.reply_text("Error: Already in a room.")
		pass
	elif room_number == "bal":
		update.message.reply_text("Error: Insufficient balance.")
		pass


def join(update, context):
	"""
  Join the room with the host room arguments.
  """
	if context.args is None:
		message = "Please type the room number that was provided to your friend. eg /join 123123"
		update.message.reply_text(message)
	else:
		check_join_room = server.join_room(context.args[0],
		                                   update.message.from_user.id)
		if (check_join_room == False):
			update.message.reply_text("Error: Already in a room.")
			pass
		elif (check_join_room == "bal"):
			update.message.reply_text("Error: Insufficient balance.")
			pass
		update.message.reply_text("You have joined room number {}".format(
		    context.args[0]))


def leave(update, context):
	"""
  Leave the room that the player is in if the player is in a room. Else no function done.
  """
	leaving = server.leave_room(update.message.from_user.id)
	if leaving == "Player not in room":
		update.message.reply_text("You are not in a room  at all!")
	elif leaving == "Player in game":
		update.message.reply_text(
		    "You are in a game right now, please finish the game first.")
	elif leaving == "Deleted Room":
		update.message.reply_text(
		    "There is no one in the room, please create or join another room.")
	elif leaving is True:
		update.message.reply_text("You have left the room")


def kick(update, context):
	"""
  Owner of the room can kick the user through inline keyboard/ reply keyboard.
  """
	roomID = db.get_users(update.message.from_user.id, "roomID")
	if roomID == [("", )]:
		update.message.reply_text("You are currently not in a room.")
		return ConversationHandler.END
	else:
		roomID = roomID[0][0]
		context.user_data['roomID'] == roomID
		players_in_room = db.get_room(roomID)
		if server.check_if_player_is_owner(update.message.from_user.id,
		                                   roomID):
			players = [player[0] for player in players_in_room]
			context.user_data['players'] = players
			update.message.reply_text("Who would you like to kick?",
			                          reply_markup=ReplyKeyboardMarkup(
			                              players, resize_keyboard=True))
			return KICKING
		else:
			update.message.reply_text(
			    "You are not the owner of the room. If you wish to remove a player, please get the owner to remove."
			)
			return ConversationHandler.END


def kicking(update, context):
	"""
  Will choose a player to be kicked from the keyboard
  """
	if update.message.text in context.user_data['players']:
		if server.kick_players(update.message.from_user.id,
		                       update.message.text,
		                       context.user_data['roomID']):
			update.message.reply_text("You have kicked the player",
			                          reply_markup=ReplyKeyboardRemove())
			return ConversationHandler.END


def force_start(update, context):
	"""
  Owner can force start the host room if there are >= 2 players or <= 9 players.
  """
	roomID = db.get_users(update.message.from_user.id, "roomID")
	if server.check_if_player_is_owner(update.message.from_user.id, roomID[0][0]):
		starting_game = server.start_game(update.message.from_user.id, roomID[0][0])
		if starting_game:
			update.message.reply_text(
			    "The room is now closed and the game will start shortly")
			for chat_id in starting_game['players'].keys():
				context.bot.send_message(chat_id = chat_id, text = "The game has started and you will be dealt your hand shortly.")
				context.bot.send_message(chat_id = chat_id, text = """
You have $<b>{}</b>.
Your hand is <b>{} {}</b>.
Cards in the middle: Empty
""".format(starting_game['players'][chat_id]['balance'], starting_game['players'][chat_id]['cards'][0], starting_game['players'][chat_id]['cards'][1]), parse_mode = ParseMode.HTML)
				if starting_game['position'][0] == chat_id:
					button_list = []
					button_list.append(InlineKeyboardButton('fold', callback_data = 'fold'))
					button_list.append(InlineKeyboardButton('all in', callback_data = 'all in'))
					button_list.append(InlineKeyboardButton('check', callback_data = 'check'))
					button_list.append(InlineKeyboardButton('50', callback_data = '50'))
					button_list.append(InlineKeyboardButton('150', callback_data = '150'))
					button_list.append(InlineKeyboardButton('250', callback_data = '250'))
					reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols = 3))
					context.bot.send_message( chat_id = chat_id, text = "What would you like to do?", reply_markup = reply_markup)

		elif type(starting_game) is list:
			update.message.reply_text("""The following users are not ready yet.
Please ask them to type /ready
{}""".format("\n".join(i) for i in starting_game),
			                          parse_mode=ParseMode.HTML)
		else:
			update.message.reply_text(
			    "Your room has already started the game. ")
			
	else:
		update.message.reply_text(
		    "You are not the owner of the room. Please get the room owner to start the game."
		)
		
def action(update, context):
	query = update.callback_query
	chat_id = query.from_user.id
	roomID = db.get_users(chat_id, "roomID")
	room = server.get_room(roomID[0][0])
	state_of_game = room['state_of_game']
	if query.data == "50" or query.data == "150" or query.data == "250":
		server.transaction(chat_id, roomID[0][0], int(query.data), state_of_game)
	room = server.get_room(roomID[0][0])
	state_of_game = room['state_of_game']

	button_list = []
	functions = ['fold','all in', 'check', '50', '150', '250']
	for i in functions:
		button_list.append(InlineKeyboardButton(i, callback_data = i))
	reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols = 3))
	position_of_current_player = server.find_index(room['position'], chat_id)
	if position_of_current_player + 1 != len(room['position']):
		next_player = room['position'][position_of_current_player + 1]
	else:
		checking = {}
		for key, value in room['players'].items():
			checking[value[state_of_game]] = []
		for key, value in room['players'].items():
			checking[value[state_of_game]].append(key)
		if len(set(checking.keys())) == 1:
			if state_of_game == "river":
				query.answer()
				winners = server.end_round(roomID[0][0])
				for pots in winners:
					pot = pots[-1]
					for winner in pots[:-1]:
						no_of_winners = len(pots) - 1
						pot = int(pot // no_of_winners)
						server.balance_transaction(winner, roomID[0][0], pot, "add")
						for player in room['position']:
							context.bot.send_message(chat_id = player, text = """
{} has won {}!
Congrats faggot""".format(room['players'][winner]['nickname'],pot))
							server.update_players_balance(player, roomID[0][0])
							context.bot.send_message(chat_id = player, text = "Your new balance: {}!".format(room['players'][player]['balance']))
				return True
			next_player = room['position'][0]
			cards_drawn = server.next_round(roomID[0][0])
			for x in room['position']:
				context.bot.send_message(chat_id = x, text = """
You have $<b>{}</b>.
Your hand is <b>{} {}</b>.
Cards in the middle: {}
""".format(room['players'][x]['balance'], room['players'][x]['cards'][0], room['players'][x]['cards'][1], " ".join(card for card in cards_drawn)), parse_mode = ParseMode.HTML)
		else:
			sorted_list = sorted(checking.keys())
			next_player = checking[sorted_list[0]][0]

	if query.data == "fold" or query.data == "all in" or query.data == "check":
		query.edit_message_text(text = "You have {}".format(query.data))
		for i in room['position']:
			if chat_id == i:
				pass
			else:
				context.bot.send_message(chat_id = i, text = "{} {}".format(room['players'][query.from_user.id]['nickname'], query.data))
	elif query.data == "50" or query.data == "150" or query.data == "250":
		query.edit_message_text(text = "You have bet {}".format(query.data))
		for i in room['position']:
			if chat_id == i:
				pass
			else:
				context.bot.send_message(chat_id = i, text = "{} has bet {}".format(room['players'][query.from_user.id]['nickname'], query.data))
	context.bot.send_message( chat_id = next_player, text = "What would you like to do?", reply_markup = reply_markup)
	server.update_room(roomID[0][0], room)
	query.answer()

def ready(update, context):
	roomID = db.get_users(update.message.from_user.id, "roomID")
	if roomID == [("", )]:
		update.message.reply_text("You are currently not in a room.")
	else:
		if server.get_ready(update.message.from_user.id, roomID[0][0]):
			update.message.reply_text(
			    "You are ready for the game! Please wait for other players to be ready as well."
			)
		else:
			update.message.reply_text(
			    "Your room might not exist or the game has already started.")


def options(update, context):
	"""
  The player can set whether they wish to receive the updates in pictures mode/text mode.  
  """
	pass

def balance(update, context):
	balance = server.retrieve_players_balance(update.message.from_user.id)
	update.message.reply_text("Your balance right now is currently {}!".format(balance))


def main():
	db.setup()
	TOKEN = "1933141887:AAG9HI6OC96Q_YfRF4Y00VU3xCdRsqulTDA"
	updater = Updater(TOKEN, use_context=True)
	dp = updater.dispatcher
	conv_start = ConversationHandler(
      entry_points=[CommandHandler("start", start)],
      states={
        CHANGE_NICKNAME: [MessageHandler(Filters.text, change_nickname)]
        
      },
      fallbacks=[CommandHandler("start", start)])
  
	dp.add_handler(CommandHandler("force_start", force_start))
	dp.add_handler(CallbackQueryHandler(action))
  
	conv_kick = ConversationHandler(
    	entry_points=[CommandHandler("kick", kick)],
    	states={KICKING: [MessageHandler(Filters.text, kicking)]},
    	fallbacks=[CommandHandler("kick", kick)])
	dp.add_handler(conv_start)
	dp.add_handler(conv_kick)
	dp.add_handler(CommandHandler("create", create))
	dp.add_handler(CommandHandler("join", join))
	dp.add_handler(CommandHandler("ready", ready))
	dp.add_handler(CommandHandler("leave", leave))
	dp.add_handler(CommandHandler("kick", kick))
	dp.add_handler(CommandHandler("force_start", force_start))
	dp.add_handler(CommandHandler("options", options))
	dp.add_handler(CommandHandler("balance", balance))
	updater.start_polling()
	updater.idle()
	
if __name__ == "__main__":
	main()
