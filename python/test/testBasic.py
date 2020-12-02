import unittest
import sys

from basicGalaxy import BasicGalaxy

from nova.engine import find

from nova.Game import Game
from nova.Player import Player
from nova.DepartureEvent import DepartureEvent
from nova.DeathProbeEvent import DeathProbeEvent
from nova.SpyProbeEvent import SpyProbeEvent
from nova.GlobalProductionEvent import GlobalProductionEvent
from nova.PurchaseSpeedEvent import PurchaseSpeedEvent
from nova.PurchaseProbeShieldEvent import PurchaseProbeShieldEvent
from nova.PurchaseDeathShieldEvent import PurchaseDeathShieldEvent

from nova.util import Log

from mx import DateTime
import log4py

class TestBasic(BasicGalaxy):
	def testPersist(self):
		games = self.store.fetchObjectsOfClass(Game, clauses="WHERE gameId = %d" % self.game.serialNum())
		self.assertEquals(len(games), 1)

		players = self.store.fetchObjectsOfClass(Player, clauses="WHERE gameId = %d" % self.game.sqlObjRef())
		self.assertEquals(len(players), 3)
		self.failUnless('kevin' in [player.name() for player in players])

	def testGameOver(self):
		"""
		Tests that an event which is scheduled to execute after the game is over will not be run
		"""
		self.game.setEndTime(DateTime.now())

		departure = DepartureEvent()
		departure.construct(self.game, DateTime.now() + DateTime.DateTimeDelta(0, 1),
							self.kevin, 20, self.corprl, self.klegg, 'Ship')

		errors = {}
		newEvents = self.processEvents([ departure ], errors)
		
		self.assertEquals(len(errors), 1)
		self.assertEquals(errors[departure], 'The game is over!')

	def testDeparture(self):
		"""
		Tests a simple successful DepartureEvent
		"""
		self.assertEquals(self.corprl.distanceTo(self.klegg), 5)
		
		departure = DepartureEvent()
		departure.construct(self.game, DateTime.now(), self.kevin, 20, self.corprl, self.klegg, 'Ship')

		newEvents = self.processEvents([ departure ])

		self.assertEquals(len(newEvents), 1)
		self.assertEquals(self.corprl.numShips(), 180)
		self.assertEquals(departure.status(), 'Complete')

		arrival = newEvents[0]

		self.assertEquals(self.corprl.distanceTo(self.klegg), 5)
		self.assertEquals(self.kevin.speed(), 0.5)
		travelTime = arrival.executionTime() - departure.executionTime()
		# 0 days, 10 hours
		self.assertEquals(travelTime, DateTime.DateTimeDelta(0, 10, 0, 0))

	def testDP(self):
		# kevin DPs pork
		# scott attempts to DP corprl but it has a death shield
		# should not be able to move ships off pork

		self.corprl.setHasDeathShield(1)

		# Should be able to move a ship off pork
		shipDeparture = DepartureEvent()
		shipDeparture.construct(self.game, DateTime.now(), self.scott, 1, self.pork, self.corprl, 'Ship')
		errors = {}
		newEvents = self.processEvents([ shipDeparture ], errors)
		self.assertEquals(len(errors), 0)

		# All scott's cash should be available
		self.assertEquals(self.scott.availableCash(), self.scott.wealth())

		departure1 = DepartureEvent()
		departure1.construct(self.game, DateTime.now(), self.kevin, 1, self.corprl, self.pork, 'DeathProbe')

		departure2 = DepartureEvent()
		departure2.construct(self.game, DateTime.now(), self.scott, 1, self.pork, self.corprl, 'DeathProbe')

		newEvents = self.processEvents([ departure1, departure2 ])

		self.assertEquals(len(newEvents), 2)
		self.assertEquals(self.corprl.numShips(), 200)
		self.assertEquals(self.pork.numShips(), 14)

		dp1 = newEvents[0]
		dp2 = newEvents[1]

		self.assertEquals(dp1.__class__, DeathProbeEvent)

		newEvents = self.processEvents([ dp1, dp2 ])
		self.assertEquals(len(newEvents), 0)
		self.failUnless(self.pork.isDead())
		self.failUnless(self.pork.owner() is self.game.nobody())
		self.failIf(self.corprl.isDead())

		self.failIf(dp1.hasDeathShield())
		self.failUnless(dp2.hasDeathShield())

		# Should no longer be able to move a ship off pork
		shipDeparture = DepartureEvent()
		shipDeparture.construct(self.game, DateTime.now(), self.scott, 1, self.pork, self.corprl, 'Ship')
		errors = {}
		newEvents = self.processEvents([ shipDeparture ], errors)
		self.assertEquals(len(errors), 1)


	def testPurchaseSPDPShield(self):
		"""
		Test success and failure of purchasing a death shield and spy shield
		"""
		self.assertEquals(self.klegg.hasSpyShield(), 0)
		self.assertEquals(self.corprl.hasDeathShield(), 0)

		# First, try and purchase shields for stars that are not owned by the player
		purchaseSpyShield = PurchaseProbeShieldEvent()
		purchaseSpyShield.construct(self.game, DateTime.now(), self.scott, self.klegg)
		purchaseDeathShield = PurchaseDeathShieldEvent()
		purchaseDeathShield.construct(self.game, DateTime.now(), self.scott, self.corprl)

		errors = {}
		newEvents = self.processEvents([ purchaseSpyShield, purchaseDeathShield ], errors)

		self.assertEquals(len(errors), 2)
		self.assertEquals(len(newEvents), 0)

		self.failUnless('Player scott does not own Corporal' in errors.values(),
			'Message not found in %s' % errors.values())

		self.assertEquals(self.klegg.hasSpyShield(), 0)
		self.assertEquals(self.corprl.hasDeathShield(), 0)

		# Now purchase the shields successfully
		purchaseSpyShield = PurchaseProbeShieldEvent()
		purchaseSpyShield.construct(self.game, DateTime.now(), self.kevin, self.klegg)
		purchaseDeathShield = PurchaseDeathShieldEvent()
		purchaseDeathShield.construct(self.game, DateTime.now(), self.kevin, self.corprl)

		errors = {}
		newEvents = self.processEvents([ purchaseSpyShield, purchaseDeathShield ], errors)
		self.assertEquals(len(errors), 0)
		self.assertEquals(len(newEvents), 0)

		self.assertEquals(self.klegg.hasSpyShield(), 1)
		self.assertEquals(self.corprl.hasDeathShield(), 1)

		# Try again. Should both fail because the stars already have shields
		# Need to give Kevin enough cash

		self.kevin.setWealth(210)
		self.store.saveChanges()	
		
		purchaseSpyShield = PurchaseProbeShieldEvent()
		purchaseSpyShield.construct(self.game, DateTime.now(), self.kevin, self.klegg)
		purchaseDeathShield = PurchaseDeathShieldEvent()
		purchaseDeathShield.construct(self.game, DateTime.now(), self.kevin, self.corprl)

		errors = {}
		newEvents = self.processEvents([ purchaseSpyShield, purchaseDeathShield ], errors)
		self.assertEquals(len(errors), 2)
		
		self.failUnless('Corporal already has a nova bomb shield' in errors.values(),
			'Message not found in %s' % errors.values())
		self.failUnless('Klegg already has a probe shield' in errors.values(),
			'Message not found in %s' % errors.values())

	def testSP(self):
		"""
		scott attempts to SP corprl and klegg
		klegg has a spy shield, corprl has a death shield
		"""

		# Make everyone's range = 5
		self.scott.setRange(5)
		self.kevin.setRange(5)

		self.klegg.setHasSpyShield(1)
		self.corprl.setHasDeathShield(1)

		departure1 = DepartureEvent()
		departure1.construct(self.game, DateTime.now(), self.scott, 1, self.pork, self.klegg, 'SpyProbe')

		departure2 = DepartureEvent()
		departure2.construct(self.game, DateTime.now(), self.scott, 1, self.pork, self.corprl, 'SpyProbe')

		errors = {}
		newEvents = self.processEvents([ departure1, departure2 ], errors)

		# Should be an error for departure1, because scott does not have enough range to make the trip
		self.assertEquals(len(errors), 1)
		self.failUnless(errors.has_key(departure1))
		self.assertEquals(len(newEvents), 1)

		# Give scott enough range and try again
		self.scott.setRange(8)

		errors = {}
		newEvents[0:0] = self.processEvents([ departure1 ], errors)
		self.assertEquals(len(errors), 0)

		# Should not change the number of ships
		self.assertEquals(len(newEvents), 2)
		self.assertEquals(self.pork.numShips(), 15)

		sp1 = newEvents[0]
		sp2 = newEvents[1]

		self.assertEquals(sp1.__class__, SpyProbeEvent)

		newEvents = self.processEvents([ sp1, sp2 ])
		self.assertEquals(len(newEvents), 0)
		
		self.failIf(self.corprl.isDead())
		self.failIf(self.klegg.isDead())

		self.failUnless(sp1.hasSpyShield())
		self.failIf(sp1.hasDeathShield())
		self.assertEquals(sp1.numShips(), 0)
		self.assertEquals(sp1.numFactories(), 0)

		self.failIf(sp2.hasSpyShield())
		self.failUnless(sp2.hasDeathShield())
		self.assertEquals(sp2.numShips(), 200)
		self.assertEquals(sp2.numFactories(), 3)

		# The 2 SpyProbe events should be reported to Scott but not to Kevin

		kevinEvents = find.getPlayerEvents(self.kevin, self.game.startTime())
		self.assertEquals(len(kevinEvents), 1)
		self.assertEquals(kevinEvents[0].uiDescription(self.kevin), "<color>Your probe shield at <star name=Klegg/> blocked a probe!</color>")

		scottEvents = find.getPlayerEvents(self.scott, self.game.startTime())
		self.assertEquals(len(scottEvents), 2)

		descriptions = [ event.uiDescription(self.scott) for event in scottEvents ]

		self.failUnless("<color>Probe Report: <star name=Klegg/></color><br/>The probe's transmission was blocked by a shield" in descriptions,
						"message not found in %s" % descriptions)
		self.failUnless("<color>Probe Report: <star name=Corporal/></color><br/>Owner:kevin, Wealth:10, Factories:3, Ships:200, " \
						"Nova Shield:Yes, Probe Shield:No" in descriptions,
						"message not found in %s" % descriptions)		

	def testPurchase(self):
		kevinWealth = self.kevin.wealth()
		
		speed = PurchaseSpeedEvent()
		# Use the convenience constructor
		speed.construct(self.game, DateTime.now(), self.kevin, 0.1)

		# Can't afford this one
		speed2 = PurchaseSpeedEvent()
		speed2.construct(self.game, DateTime.now(), self.kevin, 5)

		newEvents = self.processEvents([ speed, speed2 ])

		self.assertEquals(len(newEvents), 0)
		self.assertEquals(self.kevin.speed(), 0.6)
		self.assertEquals(len(newEvents), 0)

		self.assertEquals(speed.status(), 'Complete')
		self.assertEquals(speed2.status(), 'Invalid')

		self.assertEquals(self.kevin.wealth(), kevinWealth - 0.1 * self.game.speedCost())

	def testMinimumPurchase(self):
		"""
		Everything should cost at least $1
		"""
		kevinWealth = self.kevin.wealth()
		
		speed = PurchaseSpeedEvent()
		# Use the convenience constructor
		speed.construct(self.game, DateTime.now(), self.kevin, 0.000001)

		self.assertEquals(1, speed.cost())

	def testProduction(self):
		"""
		Execute the GlobalProductionEvent, then all the ProductionEvents that it creates
		"""
		
		# Need to speed up the game so that a production event will occur
		self.game.setTimeCompression(2)
		self.store.saveChanges()
		
		production = GlobalProductionEvent()
		production.construct(self.game, DateTime.now())

		newEvents = self.processEvents([ production ])

		# Should be 3 ProductionEvents, one for each star that has factories or wealth (Klegg has neither)
		#   plus a new GlobalProductionEvent
		# The number of factories on each star should be increased by the number of factories
		# The wealth of each player should be increased by the combined wealth of the owned stars
		self.assertEquals(len(newEvents), 3)

		self.processEvents(newEvents[:-1])

		self.assertEquals(self.corprl.numShips(), 203)
		self.assertEquals(self.klegg.numShips(), 12)
		self.assertEquals(self.pork.numShips(), 20)

		self.assertEquals(self.kevin.wealth(), 260)
		self.assertEquals(self.scott.wealth(), 258)

		# Next global production should be in 1/2 day
		newGP = newEvents[2]
		self.assertEquals(newGP.executionTime(), production.executionTime() + DateTime.DateTimeDelta(0, 12))
		self.assertEquals(newGP.status(), 'Pending')

		# GlobalProduction is reported to both players
		self.assertEquals(len(find.getPlayerEvents(self.kevin, self.game.startTime())), 1)
		self.assertEquals(len(find.getPlayerEvents(self.scott, self.game.startTime())), 1)

		self.assertEquals(production.uiDescription(self.kevin), 'Your stars produced <unit qty=3 /> and 10 cash')
		self.assertEquals(production.uiDescription(self.scott), 'Your stars produced <unit qty=5 /> and 8 cash')

if __name__=='__main__':
	log4py.Logger.instance.set_loglevel(log4py.LOGLEVEL_DEBUG)
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
