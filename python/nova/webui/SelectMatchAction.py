
from NovaPage import NovaPage
from nova.Game import Game
from nova.User import User
from nova.Player import Player
from nova.engine import store

from MiddleKit.Run.ObjectStore import UnknownObjectError

class SelectMatchAction(NovaPage):
	"""
	Once a User is logged in, they may join a match
	The userId is available as a cookie (it is set by LoginAction). The gameId is sent by the
	browser.
	
	A Player object should exist in the Game for the specified User. The gameId and playerId are
	set as cookies and the browser is redirected to the main game console
	"""
	def actions(self):
		return [ 'selectGame' ]
	
	def selectGame(self):
		userId = self.request().value('userId')
		gameId = self.request().fields()['gameId']
		dontExpire = self.request().field('dontExpireLogin', 0)
		
		user = store.get().fetchObject(User, int(userId))
		
		try:
			game = store.get().fetchObject(Game, int(gameId))
		except UnknownObjectError, x:
			return self.error('Game %d not found' % gameId)

		players = store.get().fetchObjectsOfClass(Player, "WHERE gameId = %d AND userId = %d" % ( game.sqlObjRef(), user.sqlObjRef() ))
		if not len(players):
			return self.error("'%s' is not a player in match %s" % ( user.name(), gameId))
		player = players[0]
		
		optional = {}
		if dontExpire:
			optional['expires'] = 'NEVER'
		
		self.response().setCookie('gameId', gameId, **optional)
		self.response().setCookie('playerId', player.serialNum(), **optional)
		self.response().sendRedirect('console.psp')
		
	def error(self, message):
		self.response().sendRedirect('selectMatch.psp?error=%s' % self.urlEncode(message))
