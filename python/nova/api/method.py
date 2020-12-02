import exception

from nova.engine import store
from nova.engine.Engine import Engine
from nova.Game import Game
from nova.Player import Player
from nova.Star import Star

def authenticatePlayer(game, playerName, password):
	"""
	return the Player object for the credentials, or raise a LoginException
	"""
	players = store.get().fetchObjectsOfClass(Player, clauses="WHERE gameId = %s AND name = '%s'" % ( game.sqlObjRef(), playerName) )
	if len(players) == 0 or players[0].user().password() != password:
		raise exception.LoginException("Login failed for player '%s'" % playerName)
	player = players[0]
	if player == game.nobody():
		raise exception.LoginException("You're not allowed to log in as '%s'" % game.nobody().name());
	return player

class APIMethod:
	"""
	Abstract class for implementing an API method
	If a method fails, it should return a dictionary of error messages
		The dictionary key is essentially implementation-dependent
	"""
	
	def executeEvent(self, event):
		engine = Engine(store.get())
		engine.doSavedEvents(event.game())
		return engine.execute(event)

	def abortEvent(self, event):
		engine = Engine(store.get())
		engine.doSavedEvents(event.game())
		return engine.abort(event)

	def game(self, gameId):
		"""
		The game for a gameId
		"""
		return self.findObject(Game, "WHERE gameId = %d" % gameId, "Game %s not found" % gameId)

	def login(self, game, playerName, password):
		"""
		Verifies that the playerName and password are valid for the game
		Returns the Player object
		"""
		return authenticatePlayer(game, playerName, password)

	def starName(self, starId):
		return store.get().fetchObject(Star, starId).name()

	def findStar(self, game, starName):
		return self.findObject(Star, "WHERE gameId = %s AND name = '%s'" % ( game.sqlObjRef(), starName ),
							   "Star %s not found" % starName)

	def findObject(self, cls, query, error = None, must = 1):
		list = store.get().fetchObjectsOfClass(cls, clauses=query)
		if must and len(list) == 0:
			raise exception.ObjectNotFoundException(error)
		if len(list) > 1:
			Log.warn("Found multiple %s objects %s for query %s" % ( cls, list, query ))
		return list[0]
