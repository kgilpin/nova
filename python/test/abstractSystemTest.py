import unittest, time
import sys
from mx import DateTime

from nova.DepartureEvent import travelTime
from nova.GlobalProductionEvent import GlobalProductionEvent
from nova.Game import Game
from nova.Star import Star
from nova.Player import Player

from nova.trigger.transport import DummyTransport
from nova.engine.Engine import Engine
from nova.api import dispatch, deploy
from nova.util import Log

import connection

# This is found in game.sql
GAME_ID = 1

class AbstractSystemTest(unittest.TestCase):
	"""
	System test for automated fleet deployment (automatically sending ships from one
	star to another)
	"""
	
	def setUp(self):
		self.store = connection.get()
		print 'Connected'
		self.game = self.store.fetchObject(Game, GAME_ID)
		# Game starts now and lasts for 15 minutes
		# Turn off production
		self.game.setStartTime(DateTime.now())
		self.game.setEndTime(self.game.startTime() + DateTime.DateTimeDelta(0, 0, 15))
		production = self.store.fetchObjectsOfClass(GlobalProductionEvent)[0]
		self.store.deleteObject(production)
		self.store.saveChanges()

		self.dummyEmail = DummyTransport()

	def player(self, name):
		return self.store.fetchObjectsOfClass(Player, "WHERE gameId = %s AND name = '%s'" % ( self.game.sqlObjRef(), name ) )[0]

	def star(self, name):
		return self.store.fetchObjectsOfClass(Star, "WHERE gameId = %s AND name = '%s'" % ( self.game.sqlObjRef(), name ) )[0]

	def deploy(self, playerName, origin, destination, garrison):
		"""
		Set up a deployment order from the origin to the destination
		"""
		command = deploy.DeploymentOrders()
		command.deploy(self.game.serialNum(), playerName, playerName, origin.serialNum(), destination.serialNum(), garrison)		

	def dispatch(self, playerName, origin, destination, numShips, unitType = 'Ship'):
		fleet = dispatch.DispatchFleet()
		fleet.setDelayMinutes(0)

		# print 'Sending fleet to %s' % destination.name()
		fleet.execute(self.game.serialNum(), playerName, playerName, origin.name(), destination.name(), numShips)

		self.wait(travelTime(origin, destination, self.player(playerName), unitType))
		self.engineTick()

	def wait(self, delta):
		# print 'Waiting %0.2f seconds' % ( delta.seconds )
		time.sleep(delta.seconds)
		
	def engineTick(self):
		engine = Engine(self.store)
		engine.setTransport('Email', self.dummyEmail)
		errors = engine.doSavedEvents(self.game)
		if len(errors):
			print errors
