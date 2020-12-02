import unittest
import sys

from nova.api import query
from nova.engine import find
from nova.DepartureEvent import DepartureEvent

from basicGalaxy import BasicGalaxy

from mx import DateTime

class TestQuery(BasicGalaxy):
	def testSnapshot(self):
		"""
		Constructs a bean snapshot of the game
		The snapshot includes the Game bean, plus the Star and Player beans
		"""
		snapshot = query.getSnapshot( ( self.game, self.kevin.name(), self.kevin.user().password() ) )
		self.assertEquals("kevin [ speed : 0.50, range : 10.00, income : 250, cash : 250 ]", str(snapshot.players()[0]))
		self.assertEquals("scott", str(snapshot.players()[-1]))
		self.assertEquals("Klegg [x,y : ( 15,15 ), wealth : 0, numShips : 12, numFactories : 0, hasProbeShield : 0, hasNovaShield : 0]", str(snapshot.stars()[1]))
		self.assertEquals("Pork [x,y : ( 10,10 )]", str(snapshot.stars()[2]))
	
	def testFleetSnapshot(self):
		"""
		Gets a snapshot of the game, including fleets
		"""
		departure = DepartureEvent()
		departure.construct(self.game, DateTime.now(), self.kevin, 20, self.corprl, self.klegg, 'Ship')
		self.processEvents([ departure ])

		self.assertEquals(len(find.getPlayerFleetsInTransit(self.kevin)), 1)
		self.assertEquals(len(find.getPlayerFleetsInTransit(self.scott)), 0)
		
		# Get all the events
		snapshot = query.getSnapshot(self.kevin)
		self.assertEquals(1, len(snapshot.fleets()))
		
		# Construct a Probe DepartureEvent 10 minutes in the future
		# Should still see it
		departure = DepartureEvent()
		departure.construct(self.game, DateTime.now() + DateTime.DateTimeDelta(0, 0, 10), self.kevin, 1, self.corprl, self.klegg, 'SpyProbe')
		self.processEvents([ departure ])

		snapshot = query.getSnapshot(self.kevin)
		fleet = snapshot.fleets()[0]
		self.failUnless(str(fleet).endswith("kevin sending 1 Probe from Corporal to Klegg"), fleet)
		fleet = snapshot.fleets()[1]
		self.failUnless(str(fleet).endswith("kevin sending 20 Ship from Corporal to Klegg"), fleet)
		
	def testStars(self):
		self.assertEquals(len(find.getAllStars(self.game)), 3)
		self.assertEquals(len(find.getOwnedLiveStars(self.kevin)), 2)
		self.assertEquals(len(find.getOwnedLiveStars(self.scott)), 1)

	def testFleets(self):
		departure = DepartureEvent()
		departure.construct(self.game, DateTime.now(), self.kevin, 20, self.corprl, self.klegg, 'Ship')
		self.processEvents([ departure ])

		self.assertEquals(len(find.getPlayerFleetsInTransit(self.kevin)), 1)
		self.assertEquals(len(find.getPlayerFleetsInTransit(self.scott)), 0)

		# Set the DepartureEvent's arrivalTime to one second after Now. 
		# It should not show as completed yet though because the game's
		#   lastActionTime shows that it has not been processed yet
		departure.setArrivalTime(DateTime.now())
		self.game.setLastActionTime(DateTime.now() - DateTime.DateTimeDelta(0, 0, 0, 1))
		self.store.saveChanges()

		self.assertEquals(len(find.getPlayerFleetsInTransit(self.kevin)), 1)
		
		# If we change the game's lastActionTime to be the same as the DepartureEvent's arrival time
		#   the query will tell us that the fleet has arrived
		self.game.setLastActionTime(departure.arrivalTime())
		self.store.saveChanges()
		self.assertEquals(len(find.getPlayerFleetsInTransit(self.kevin)), 0)		

if __name__=='__main__':
	loader = unittest.TestLoader()
	if len(sys.argv) > 1:
		suite = loader.loadTestsFromName(sys.argv[1], module=TestQuery)
	else:
		suite = loader.loadTestsFromTestCase(TestQuery)
	testRunner = unittest.TextTestRunner()
	result = testRunner.run(suite)
	sys.exit(not result.wasSuccessful())
"""
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
"""