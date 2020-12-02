'''
PurchaseSpeedEvent.py
'''

import PurchaseEvent

from GeneratedPy.GenPurchaseSpeedEvent import GenPurchaseSpeedEvent
from nova.Exceptions import InvalidEventException

class PurchaseSpeedEvent(GenPurchaseSpeedEvent):
	def construct(self, game, executionTime, player, delta):
		GenPurchaseSpeedEvent.construct(self, game, executionTime, player, game.speedCost() * delta, delta)

	def validate(self):
		GenPurchaseSpeedEvent.validate(self)
		if self.delta() < 0:
			raise InvalidEventException("You can't purchase a negative amount ( %s )" % self.itemDescription())

	def itemDescription(self):
		return "%.2f speed" % ( self.delta() * self.game().timeCompression() )

	def execute(self):
		self.player().setSpeed(self.player().speed() + self.delta())
		GenPurchaseSpeedEvent.execute(self)
