'''
PurchaseDeathShieldEvent.py
'''


from nova.Exceptions import InvalidEventException
from Event import Event

from GeneratedPy.GenPurchaseDeathShieldEvent import GenPurchaseDeathShieldEvent

class PurchaseDeathShieldEvent(GenPurchaseDeathShieldEvent):

	def __init__(self):
		GenPurchaseDeathShieldEvent.__init__(self)

	def construct(self, game, executionTime, player, star):
		GenPurchaseDeathShieldEvent.construct(self, game, executionTime, player, game.deathShieldCost(), star)

	def itemDescription(self):
		return "a nova bomb shield on %s" % self.star().name()

	def validate(self):
		GenPurchaseDeathShieldEvent.validate(self)
		Event.validateOwner(self, self.star())
		if self.star().hasDeathShield():
			raise InvalidEventException('%s already has a nova bomb shield' % self.star().name())

	def execute(self):
		self.star().setHasDeathShield(1)
		GenPurchaseDeathShieldEvent.execute(self)
