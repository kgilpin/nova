import unittest
import sys, time
import log4py

from nova.util import Log
from nova.DepartureEvent import DepartureEvent
from nova.api import dispatch, purchase, query, notifications
from nova.engine import find
from nova.api.exception import LoginException
from basicGalaxy import BasicGalaxy

from mx import DateTime

class TestAPI(BasicGalaxy):
	def testBadPassword(self):
		exception = None
		fleet = dispatch.DispatchFleet()

		self.failUnlessRaises(LoginException, fleet.execute, self.game.serialNum(), self.kevin.name(), 'fooz', None, None, None)

	def testFleet(self):
		"""
		Tests basic dispatching of a fleet
		"""
		fleet = dispatch.DispatchFleet()
		errors = fleet.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
										  self.klegg.name(), 20)
		self.assertEquals(len(errors), 0)
		self.assertEquals(self.corprl.numShips(), 180)

	def testTooLate(self):
		"""
		Test that a fleet cannot be sent if it will arrive too late
		"""
		self.game.setEndTime(DateTime.now())
		self.store.saveChanges()
		
		fleet = dispatch.DispatchFleet()
		errors = fleet.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
										  self.klegg.name(), 20)
		self.assertEquals(len(errors), 1)
		self.assertEquals(errors.values()[0], 'There is not enough time left in the game')

	def testNovaVisibility(self):
		"""
		A DP which is blocked by a shield should not be visible to a third player
		"""
		self.game.setTimeCompression(50000)
		self.pork.setOwner(self.game.nobody())
		self.pork.setHasDeathShield(1)
		self.store.saveChanges()
		
		dp = dispatch.DispatchDeathProbe()
		errors = dp.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
										  self.pork.name())
		self.assertEquals(len(errors), 0)

		# Wait for the event to be processable, then run it
		time.sleep(0.75)
		
		self.doSavedEvents()

		# DP should show up for kevin, but not for scott (because Nobody owns Pork)
		events = find.getPlayerEvents(self.kevin, self.game.startTime())
		self.assertEquals(len(events), 1)
		
		events = find.getPlayerEvents(self.scott, self.game.startTime())
		self.assertEquals(len(events), 0)

	def testPendingCost(self):
		"""
		Test sending a delayed spy probe
		The player's available cash should be reduced while the departure is pending
		Should work for a DP as well
		Try and send another delayed DP
			Should not be allowed because kevin does not have enough available cash
		Try and buy factories
			Should not be allowed because kevin does not have enough available cash
		"""
		sp = dispatch.DispatchSpyProbe()
		sp.setDelayMinutes(2)
		errors = sp.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
			self.pork.name())
		self.assertEquals(len(errors), 0)
		self.assertEquals(self.kevin.availableCash(), self.kevin.wealth() - self.game.spyProbeCost())

		dp = dispatch.DispatchDeathProbe()
		dp.setDelayMinutes(2)
		errors = dp.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
			self.pork.name())
		self.assertEquals(len(errors), 0)
		self.assertEquals(self.kevin.availableCash(), self.kevin.wealth() - self.game.spyProbeCost() - self.game.deathProbeCost())

		dp = dispatch.DispatchDeathProbe()
		dp.setDelayMinutes(2)
		errors = dp.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
			self.pork.name())
		self.assertEquals(len(errors), 1)
		self.assertEquals(errors.values()[0], "Player kevin cannot afford $200 for a Death Probe")

		# Have 210 in pending cost, should have $40 left over
		# Should be able to by 8 factories, but not 9
		
		buy = purchase.PurchaseFactories()
		errors = buy.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(), 9)
		self.assertEquals(len(errors), 1)

		buy = purchase.PurchaseFactories()
		errors = buy.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(), 8)
		self.assertEquals(len(errors), 0)
	
	def testDelay(self):
		"""
		Send a fleet delayed by 5 minutes
		Test that the fleet is identified as a fleet in transit
		Test that the ships scheduled for departure are identified
		Then abort it
		"""
		fleet = dispatch.DispatchFleet()
		fleet.setDelayMinutes(5)
		now = DateTime.now()
		
		self.assertEquals(self.corprl.numAvailableShips(), self.corprl.numShips())
		
		errors = fleet.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
										  self.klegg.name(), 20)
		self.assertEquals(len(errors), 0)
		departure = self.store.fetchObjectsOfClass(DepartureEvent, clauses="WHERE gameId = %s" % self.game.sqlObjRef())[0]
		self.failUnless(departure.executionTime() >= now + DateTime.DateTimeDelta(0, 0, 4.5),
						"Expected departure time %s to be about 5 minutes after %s" % ( departure.executionTime(), now) )

		self.assertEquals(departure.status(), 'Pending')
		self.assertEquals(len(find.getPlayerFleetsInTransit(self.kevin)), 1)	

		pendingShips = find.getPendingShipsByStar(self.game)
		# Should be one entry for each star
		self.assertEquals(len(pendingShips), self.numStars)
		self.assertEquals(pendingShips[self.corprl.serialNum()], 20)
		self.assertEquals(pendingShips[self.pork.serialNum()], 0)
		self.assertEquals(pendingShips[self.klegg.serialNum()], 0)
		
		# Try and send all of Corporal's ships, and test that it fails because there are not enough
		#   available
		self.assertEquals(self.corprl.numAvailableShips(), self.corprl.numShips() - 20)
		fleet = dispatch.DispatchFleet()
		errors = fleet.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
										  self.klegg.name(), self.corprl.numShips())
		self.assertEquals(len(errors), 1)
		self.assertEquals(errors.values()[0], "Star Corporal (180 ships) does not have 200 ships to send")
		
		abort = dispatch.Abort()
		errors = abort.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), departure.serialNum())
		self.assertEquals(len(errors), 0)										  
		self.assertEquals(len(find.getPlayerFleetsInTransit(self.kevin)), 0)	

		self.assertEquals(self.corprl.numAvailableShips(), self.corprl.numShips())
		pendingShips = find.getPendingShipsByStar(self.game)
		self.assertEquals(pendingShips[self.corprl.serialNum()], 0)

		# Send them all away again, there should be no errors
		fleet = dispatch.DispatchFleet()
		errors = fleet.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
										  self.klegg.name(), self.corprl.numShips())
		self.assertEquals(len(errors), 0)										  

	def testFailAbort(self):
		"""
		Fail to abort an event which has already been processed
		"""
		fleet = dispatch.DispatchFleet()
		errors = fleet.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
										  self.klegg.name(), 20)
		self.assertEquals(len(find.getPlayerFleetsInTransit(self.kevin)), 1)	

		departure = self.store.fetchObjectsOfClass(DepartureEvent, clauses="WHERE gameId = %s" % self.game.sqlObjRef())[0]
		self.assertEquals(departure.status(), 'Complete')
		abort = dispatch.Abort()
		errors = abort.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), departure.serialNum())
		self.assertEquals(len(errors), 1)										  
		self.assertEquals(len(find.getPlayerFleetsInTransit(self.kevin)), 1)	

	def testAbortRouting(self):
		"""
		Abort a DepartureEvent which has already been executed, but which specifies a long-distance routing.
		The finalDestination should be set to the name of the destination of the last leg
		"""
		
		# Set kevin's range to 5
		# Set Pork.owner = Kevin
		# Send a fleet from Pork to Klegg, should route through Corporal
		self.kevin.setRange(5)
		self.pork.setNumShips(20)
		self.pork.setOwner(self.kevin)
		self.store.saveChanges()
		
		fleet = dispatch.DispatchFleet()
		errors = fleet.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.pork.name(),
										  self.klegg.name(), 20)
		self.assertEquals(0, len(errors), errors)

		departure = self.store.fetchObjectsOfClass(DepartureEvent, clauses="WHERE gameId = %s" % self.game.sqlObjRef())[0]
		self.assertEquals(departure.status(), 'Complete')
		self.assertEquals(departure.destination(), self.corprl, departure)
		self.assertEquals(departure.finalDestination(), self.klegg, departure)

		abort = dispatch.Abort()
		errors = abort.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), departure.serialNum())
		self.assertEquals(0, len(errors), errors)										  

		# Re-load the event
		departure = self.store.fetchObjectsOfClass(DepartureEvent, clauses="WHERE departureEventId = %s" % departure.serialNum(), refreshAttrs = 1)[0]
		self.assertEquals(departure.destination(), self.corprl, departure)
		self.assertEquals(departure.finalDestination(), self.corprl, departure)

	def testPurchaseShields(self):
		"""
		Test purchasing a probe shield and a death shield
		"""
		probeShield = purchase.PurchaseProbeShield()
		errors = probeShield.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.klegg.name())
		self.assertEquals(len(errors), 0)

		deathShield = purchase.PurchaseDeathShield()
		errors = deathShield.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name())
		self.assertEquals(len(errors), 0)
		
	def testScores(self):
		"""
		Tests querying for player scores
		"""
		scores = find.getPlayerScores(self.game)
		self.assertEquals(len(scores), 2)
		self.assertEquals(scores[0], ( 'kevin', 2 ))
		self.assertEquals(scores[1], ( 'scott', 1 ))
		
		self.corprl.setOwner(self.scott)
		self.klegg.setOwner(self.nobody)
		self.store.saveChanges()		

		scores = find.getPlayerScores(self.game)
		self.assertEquals(len(scores), 2)
		self.assertEquals(scores[0], ( 'scott', 2 ))
		self.assertEquals(scores[1], ( 'kevin', 0 ))
		
	def testBattleNotification(self):
		"""
		Tests enabling and disabling battle notification messages
		"""
		
		self.assertEquals(0, find.isBattleNotificationEnabled(self.kevin))
		notifications.BattleNotification().enable(self.game.serialNum(), self.kevin.name(), self.kevin.user().password())
		self.assertEquals(1, find.isBattleNotificationEnabled(self.kevin))
		# Re-enabling should be a no-op
		notifications.BattleNotification().enable(self.game.serialNum(), self.kevin.name(), self.kevin.user().password())
		self.assertEquals(1, find.isBattleNotificationEnabled(self.kevin))
		notifications.BattleNotification().disable(self.game.serialNum(), self.kevin.name(), self.kevin.user().password())
		self.assertEquals(0, find.isBattleNotificationEnabled(self.kevin))
		# Re-disabling should be a no-op
		notifications.BattleNotification().disable(self.game.serialNum(), self.kevin.name(), self.kevin.user().password())
		self.assertEquals(0, find.isBattleNotificationEnabled(self.kevin))
		
if __name__=='__main__':
	#Log.enabled = 1
	#log4py.Logger().get_instance("DepartureEvent").set_loglevel(log4py.LOGLEVEL_DEBUG)

	loader = unittest.TestLoader()
	if len(sys.argv) > 1:
		suite = loader.loadTestsFromName(sys.argv[1], module=TestAPI)
	else:
		suite = loader.loadTestsFromTestCase(TestAPI)
	testRunner = unittest.TextTestRunner()
	result = testRunner.run(suite)
	sys.exit(not result.wasSuccessful())
