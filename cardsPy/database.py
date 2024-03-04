import sqlite3
"""
Players: nickname, roomID chatID, balance, gamesPlayed, gamesWon, level
"""


class DBHelper:
	def __init__(self, dbname="database.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname, check_same_thread=False)

	def setup(self):
		stmt = "CREATE TABLE IF NOT EXISTS Players (playersID INTEGER PRIMARY KEY AUTOINCREMENT, nickname varchar(20), roomID varchar(6), chatID INTEGER UNIQUE, balance INTEGER, gamesPlayed INTEGER, gamesWon INTEGER, level INTEGER)"
		try:
			self.conn.execute(stmt)
			self.conn.commit()
			self.reset_roomIDs()
		except sqlite3.Error as er:
			print('SQLite error: %s' % (' '.join(er.args)))

	def reset_roomIDs(self):
		stmt = "UPDATE Players SET roomID = ''"
		try:
			self.conn.execute(stmt)
			self.conn.commit()
		except sqlite3.Error as er:
			print('SQLite error: %s' % (' '.join(er.args)))

	def add_users(self,
	              nickname,
	              chatID,
	              balance=1000,
	              gamesPlayed=0,
	              gamesWon=0,
	              level=1):  #WIP
		if (self.get_users(chatID, "all") != []):
			# chatid alr exists then return user?
			return False
		else:
			stmt = "INSERT OR IGNORE INTO Players (nickname, roomID, chatID, balance, gamesPlayed, gamesWon, level) VALUES (?, ?, ?, ?, ?, ?, ?)"
			args = (nickname, "", chatID, balance, gamesPlayed, gamesWon,
			        level)
			try:
				self.conn.execute(stmt, args)
				self.conn.commit()
				return True
			except sqlite3.Error as er:
				print('SQLite error: %s' % (' '.join(er.args)))

	def get_users(self, chatID, type):  #WIP
		stmt = ""
		if type == "all":
			stmt = "SELECT * FROM Players WHERE chatID = (?)"
		elif type == "roomID":
			stmt = "SELECT roomID FROM Players WHERE chatID = (?)"
		elif type == "nickname":
			stmt = "SELECT nickname FROM Players WHERE chatID = (?)"
		elif type == "balance":
			stmt = "SELECT balance FROM Players WHERE chatID = (?)"
		elif type == "gamesPlayed" or type == "gamesWon" or type == "level":
			stmt = "SELECT gamesPlayed, gamesWon, level FROM Players WHERE chatID = (?)"
		args = (chatID, )
		try:
			players = self.conn.execute(stmt, args)
			return players.fetchall()
		except sqlite3.Error as er:
			print('SQLite error: %s' % (' '.join(er.args)))

	def get_room(self, roomID):  #WIP
		stmt = "SELECT * FROM Players WHERE roomID = (?)"
		args = (roomID, )
		try:
			players_in_room = self.conn.execute(stmt, args)
			return players.fetchall()
		except sqlite3.Error as er:
			print("SQLite error: %s" % (' '.join(er.args)))

	def edit_users(self, chatID, type, data):
		stmt = ""
		if type == "roomID":
			stmt = "UPDATE Players SET roomID = (?) WHERE chatID = (?)"
		elif type == "balance":
			stmt = "UPDATE Players SET balance = (?) WHERE chatID = (?)"
		args = (data, chatID)
		try:
			self.conn.execute(stmt, args)
			self.conn.commit()
			return True

		except sqlite3.Error as er:
			print('SQLite error: %s' % (' '.join(er.args)))
			return False