'''
PurchaseProbeShieldEvent.py
'''

from nova.Exceptions import InvalidEventException
from Event import Event

from GeneratedPy.GenPurchaseProbeShieldEvent import GenPurchaseProbeShieldEvent

class PurchaseProbeShieldEvent(GenPurchaseProbeShieldEvent):

	def __init__(self):
		GenPurchaseProbeShieldEvent.__init__(self)

	def construct(self, game, executionTime, player, star):
		GenPurchaseProbeShieldEvent.construct(self, game, executionTime, player, game.probeShieldCost(), star)

	def itemDescription(self):
		return "a probe shield on %s" % self.star().name()

	def validate(self):
		GenPurchaseProbeShieldEvent.validate(self)
		Event.validateOwner(self, self.star())
		if self.star().hasSpyShield():
			raise InvalidEventException('%s already has a probe shield' % self.star().name())

	def execute(self):
		self.star().setHasSpyShield(1)
		GenPurchaseProbeShieldEvent.execute(self)
		