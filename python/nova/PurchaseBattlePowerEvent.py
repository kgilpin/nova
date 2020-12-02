'''
PurchaseBattlePowerEvent.py
'''

from GeneratedPy.GenPurchaseBattlePowerEvent import GenPurchaseBattlePowerEvent
from nova.Exceptions import InvalidEventException

class PurchaseBattlePowerEvent(GenPurchaseBattlePowerEvent):
	def construct(self, game, executionTime, player, delta):
		GenPurchaseBattlePowerEvent.construct(self, game, executionTime, player,
														  game.battlePowerCost() * delta, delta)

	def validate(self):
		GenPurchaseBattlePowerEvent.validate(self)
		if self.delta() < 0:
			raise InvalidEventException("You can't purchase a negative amount ( %s )" % self.itemDescription())

	def itemDescription(self):
		return "%.2f battle power" % self.delta()

	def execute(self):
		self.player().setBattlePower(self.player().battlePower() + self.delta())
		GenPurchaseBattlePowerEvent.execute(self)
