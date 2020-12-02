'''
PurchaseFactoriesEvent.py
'''

import PurchaseEvent

from GeneratedPy.GenPurchaseFactoriesEvent import GenPurchaseFactoriesEvent

class PurchaseFactoriesEvent(GenPurchaseFactoriesEvent):
	def construct(self, game, executionTime, player, star, delta):
		GenPurchaseFactoriesEvent.construct(self, game, executionTime, player, game.factoryCost() * delta, star, delta)

	def validate(self):
		"""
		Verify that the star is not dead
		"""
		GenPurchaseFactoriesEvent.validate(self)
		if self.star().isDead():
			raise InvalidEventException('Star %s is dead!' % self.origin().name())

	def itemDescription(self):
		return "%d factories" % self.delta()

	def execute(self):
		self.star().setNumFactories(self.star().numFactories() + self.delta())
		GenPurchaseFactoriesEvent.execute(self)

