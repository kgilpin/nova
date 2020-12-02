import os

from NovaPage import NovaPage
from nova.User import User
from nova.engine import mapLoader, newGame

from mx import DateTime

class NewGameAction(NovaPage):
	def actions(self):
		return [ 'newGame' ]
	
	def newGame(self):
		userSerialNumbers = self.request().fields()['users']
		mapName = self.request().fields()['map']
		timeCompression = float(self.request().fields()['timeCompression'])

		users = [ self.store().fetchObject(User, int(sn)) for sn in userSerialNumbers ]

		loader = mapLoader.ImageMapLoader(os.path.join(self.mapDir(), mapName))
		starMap = loader.loadStarMap()
		
		# Create a new game which runs for 21 days
		game = newGame.NewGame(starMap, users, DateTime.now(), DateTime.DateTimeDelta(21) / timeCompression, self.store(),
							   timeCompression=timeCompression).game()

		self.response().setCookie('gameId', game.serialNum())
		
		self.response().sendRedirect('console.psp')
		return
