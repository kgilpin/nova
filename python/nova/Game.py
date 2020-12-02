'''
Game.py
'''


from Player import Player
from GlobalProductionEvent import nextProductionTime
from nova.bean import game

from GeneratedPy.GenGame import GenGame

from mx import DateTime

class Game(GenGame):
	def __init__(self):
		GenGame.__init__(self)

	def createBean(self, beanContext):
		"""
		Construct a Game bean
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		currentTime = DateTime.now()
		return game.Game().construct(self.serialNum(), self.startTime(), self.endTime(), currentTime, nextProductionTime(currentTime, self), \
			   self.deathProbeCost(), self.spyProbeCost(), self.factoryCost(), self.speedCost(), self.rangeCost(), self.probeShieldCost(), \
			   self.deathShieldCost(), self.timeCompression())

	def nobody(self):
		"""
		Return the 'Nobody' player for the game
		"""
		return self._mk_store.fetchObjectsOfClass(Player, clauses="WHERE gameId = %d AND name = 'Nobody'" % self.sqlObjRef())[0]
