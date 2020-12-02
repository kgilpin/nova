'''
PurchaseRangeEvent.py
'''

import PurchaseEvent

from GeneratedPy.GenPurchaseRangeEvent import GenPurchaseRangeEvent
from nova.Exceptions import InvalidEventException

class PurchaseRangeEvent(GenPurchaseRangeEvent):
	def construct(self, game, executionTime, player, delta):
		GenPurchaseRangeEvent.construct(self, game, executionTime, player, game.rangeCost() * delta, delta)

	def validate(self):
		GenPurchaseRangeEvent.validate(self)
		if self.delta() < 0:
			raise InvalidEventException("You can't purchase a negative amount ( %s )" % self.itemDescription())

	def itemDescription(self):
		return "%.2f range" % self.delta()

	def execute(self):
		self.player().setRange(self.player().range() + self.delta())
		GenPurchaseRangeEvent.execute(self)
