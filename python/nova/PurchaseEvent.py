'''
PurchaseEvent.py
'''

from nova.util import Log

from Event import Event
from GeneratedPy.GenPurchaseEvent import GenPurchaseEvent

class PurchaseEvent(GenPurchaseEvent):
	def itemDescription(self):
		"""
		Should return a description of what is being purchased
		"""
		raise NotImplementedError, self.__class__

	def validate(self):
		"""
		Verify that the player has enough money to fund the purchaseEvent
		"""
		Event.validateCost(self, self.cost(), self.itemDescription())

	def cost(self):
		cost = GenPurchaseEvent.cost(self)
		if cost <= 1:
			cost = 1
		return cost

	def execute(self):
		self.player().subtractWealth( int(self.cost()) )
		Log.log('Player ', self.player().name(), ' spent ', self.cost(), ' on ', self.itemDescription(),
				  '. Has ', self.player().wealth(), ' remaining')

