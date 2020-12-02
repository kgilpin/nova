
from nova.engine.Engine import Engine
from nova.Game import Game
from nova.Player import Player
from nova.Star import Star
from nova.User import User

from nova.util import Log

import novaTest
import connection

from MiddleKit.Run.MySQLObjectStore import MySQLObjectStore

from mx import DateTime

class BasicGalaxy(novaTest.NovaTest):
	def doSavedEvents(self, emailProcessor = None):
		engine = Engine(self.store)
		if emailProcessor is not None:
			engine.setTransport('Email', emailProcessor)
		return engine.doSavedEvents(self.game)
		
	def processEvents(self, events, errors={}):
		engine = Engine(self.store)
		return engine.processEvents(events, errors)

	def setUp(self):
		self.store = connection.get()

		game = Game()
		# Construct a game that ends one day from now
		game.construct(DateTime.now(), DateTime.now() + DateTime.DateTimeDelta(1))

		kUser = self.makeUser('kevin', 'kevin', 'kgilpin@yahoo.com')
		sUser = self.makeUser('scott', 'scott', 'bze3m8mp@verizon.net')
		nUser = self.makeUser('Nobody', '', '')
		
		kevin = Player()
		kevin.construct(game, kUser, 'kevin')

		scott = Player()
		scott.construct(game, sUser, 'scott')

		nobody = Player()
		nobody.construct(game, nUser, 'Nobody')

		corprl = Star()
		corprl.construct(game, 'Corporal', 10, 15)
		corprl.setOwner(kevin)
		corprl.setWealth(10)
		corprl.setNumFactories(3)
		corprl.setNumShips(200)

		klegg = Star()
		klegg.construct(game, 'Klegg', 15, 15)
		klegg.setOwner(kevin)
		klegg.setWealth(0)
		klegg.setNumShips(12)

		pork = Star()
		pork.construct(game, 'Pork', 10, 10)
		pork.setOwner(scott)
		pork.setWealth(8)
		pork.setNumFactories(5)
		pork.setNumShips(15)

		self.game = game
		self.kUser = kUser
		self.sUser = sUser
		self.nUser = nUser
		self.kevin = kevin
		self.scott = scott
		self.nobody = nobody
		self.corprl = corprl
		self.klegg = klegg
		self.pork = pork
		
		self.numStars = 3

		self.store.addObject(self.game)
		self.store.addObject(self.kUser)
		self.store.addObject(self.sUser)
		self.store.addObject(self.nUser)
		self.store.addObject(self.kevin)
		self.store.addObject(self.scott)
		self.store.addObject(self.nobody)
		self.store.addObject(self.corprl)
		self.store.addObject(self.klegg)
		self.store.addObject(self.pork)
		self.store.saveChanges()



		
