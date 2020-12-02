import unittest, time
import sys
from mx import DateTime

from nova.DepartureEvent import travelTime
from nova.util import Log
from nova.api import query

import abstractSystemTest

# This is found in game.sql
GAME_ID = 1

class SystemSnapshot(abstractSystemTest.AbstractSystemTest):
	"""
	Tests submitting all kinds of actions and retrieving the game snapshot
	"""

	def testSnapshot(self):
		"""
		Tests BattleEvent and ArrivalEvent messages
		Tests eventLimit
		"""
		
		# First dispatch 50 ships from Kevin to Beid
		kevin = self.star("Kevin")
		beid = self.star("Beid")
		alderamin = self.star("Alderamin")
		bogardus = self.star("Bogardus")

		self.dispatch("kevin", kevin, beid, 50)

		# Now dispatch another 50 ships from Kevin to Alderamin
		# These should be routed through Beid
		self.dispatch("kevin", kevin, alderamin, 50)
		self.wait(travelTime(beid, alderamin, self.player('kevin'), 'Ship'))
		self.engineTick()

		# Now dispatch another 50 ships from Kevin to Bogardus
		# These should be routed through Beid
		self.dispatch("kevin", kevin, bogardus, 50)
		self.wait(travelTime(beid, bogardus, self.player('kevin'), 'Ship'))
		self.engineTick()
		
		# There should be 3 battle events. Check them from the perspective of 2 players
		snapshot = query.getSnapshot(self.player('kevin'), since=self.game.startTime())
		events = snapshot.events()
		self.assertEquals(5, len(events))
		event = events[0]
		self.failUnless(event.uiDescription().startswith('<unit qty=50 /> attacked <star name=Bogardus/> (owner Nobody, <unit qty=16 />)<br/>You won the battle'))

		snapshot = query.getSnapshot(self.player('dave'), since=self.game.startTime())
		events = snapshot.events()
		self.assertEquals(3, len(events))
		event = events[0]
		self.assertEquals('<i>kevin captured <star name=Bogardus/> (from Nobody)</i>', event.uiDescription())

		# Just the last 2 events		
		snapshot = query.getSnapshot(self.player('kevin'), since=self.game.startTime(), eventLimit = 2)
		events = snapshot.events()
		self.assertEquals(2, len(events))
		

if __name__=='__main__':
	# Log.enabled = 1
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
