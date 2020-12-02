import unittest, time
import sys
from mx import DateTime

from nova.DepartureEvent import travelTime

from nova.engine.Engine import Engine
from nova.util import Log

import abstractSystemTest

# This is found in game.sql
GAME_ID = 1

class SystemRouting(abstractSystemTest.AbstractSystemTest):
	"""
	System test for Nova fleet routing
	"""

	def testFleetRouting(self):
		"""
		Test that player 'kevin' can dispatch a fleet across multiple stars, which uses the FleetRoutingTrigger
		"""
		
		# First dispatch 50 ships from Kevin to Beid
		kevin = self.star("Kevin")
		beid = self.star("Beid")
		alderamin = self.star("Alderamin")
		bogardus = self.star("Bogardus")

		self.assertEquals(beid.owner(), self.player("Nobody"))
			
		self.dispatch("kevin", kevin, beid, 50)

		self.assertEquals(beid.owner(), self.player("kevin"))		

		# Now dispatch another 50 ships from Kevin to Alderamin
		# These should be routed through Beid
		self.dispatch("kevin", kevin, alderamin, 50)
		self.wait(travelTime(beid, alderamin, self.player('kevin'), 'Ship'))
		self.engineTick()
		self.assertEquals(alderamin.owner(), self.player("kevin"))

		# Now dispatch another 50 ships from Kevin to Bogardus
		# These should be routed through Beid
		self.dispatch("kevin", kevin, bogardus, 50)
		self.wait(travelTime(beid, bogardus, self.player('kevin'), 'Ship'))
		self.engineTick()
		self.assertEquals(bogardus.owner(), self.player("kevin"))

if __name__=='__main__':
	# Log.enabled = 1
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
