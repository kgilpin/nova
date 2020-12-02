# Gain access to the nova package
import unittest
import os, sys
import log4py

from basicGalaxy import BasicGalaxy

import nova
from nova.engine import find
from nova.DepartureEvent import DepartureEvent
from nova.ArrivalEvent import ArrivalEvent
from nova.BattleEvent import BattleEvent

from nova.util import Log

from mx import DateTime

class OneThenZeros:
	"""
	Return a 1, and then 'n' zeros
	"""
	def __init__(self, n):
		self.results = [ 1 ] + [ 0 for i in range(n) ]
	
	def __call__(self):
		return self.results.pop(0)

class TestBattle(BasicGalaxy):
	def testBattle(self):
		"""
		Kevin attacks Pork from Corprl with 20 ships
		The defender wins the battle
		"""
		departure = DepartureEvent()
		numAttackingShips = 20
		departure.construct(self.game, DateTime.now(), self.kevin, numAttackingShips, self.corprl, self.pork, 'Ship')

		newEvents = self.processEvents([ departure ])

		self.assertEquals(len(newEvents), 1)
		arrival = newEvents[0]
		self.assertEquals(arrival.__class__, ArrivalEvent)
		self.assertEquals(arrival.departureEvent(), departure)

		# The defender will lose the first battle and then win the rest
		nova.BattleEvent.randomSequence = OneThenZeros(numAttackingShips)
		try:
			newEvents = self.processEvents([ arrival ])
	
			self.assertEquals(len(newEvents), 1)
			battle = newEvents[0]
			self.assertEquals(battle.__class__, BattleEvent)
	
			newEvents = self.processEvents([ battle ])
			self.assertEquals(len(newEvents), 0)
	
			# Scott should win the battle with 14 ships remaining
			self.assertEquals(battle.victor(), self.scott)
			self.assertEquals(battle.numShipsLost(), 1)
			self.assertEquals(battle.star().numShips(), 14)
	
			# Both players should see the battle
			self.assertEquals(len(find.getPlayerEvents(self.kevin, self.game.startTime())), 1)
			self.assertEquals(len(find.getPlayerEvents(self.scott, self.game.startTime())), 1)
	
			reportedEvents = find.getPlayerEvents(self.scott, self.game.startTime())
			descriptions = [ event.uiDescription(self.scott) for event in reportedEvents ]
	
			self.failUnless('<color>kevin attacked <star name=Pork/> with <unit qty=20 />!</color><br/>You had <unit qty=15 /> stationed there at the time<br/>You won the battle, with <unit qty=14 /> remaining' in descriptions,
							'message not found in %s ' % descriptions)
	
			reportedEvents = find.getPlayerEvents(self.kevin, self.game.startTime())
			descriptions = [ event.uiDescription(self.kevin) for event in reportedEvents ]
	
			self.failUnless('<unit qty=20 /> attacked <star name=Pork/> (owner scott, <unit qty=15 />)<br/>scott won the battle, with <unit qty=14 /> remaining' in descriptions,
							'message not found in %s ' % descriptions)
		finally:
			nova.BattleEvent.randomSequence = None

if __name__=='__main__':
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
