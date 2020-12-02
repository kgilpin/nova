'''
SpyProbeEvent.py
'''

from nova.bean import event
from GeneratedPy.GenSpyProbeEvent import GenSpyProbeEvent

class SpyProbeEvent(GenSpyProbeEvent):
	def createBean(self, beanContext):
		"""
		Construct an ProbeEvent bean
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		starInfo = None
		if not self.hasSpyShield():
			starInfo = self.star().createStarOwnerInfo(beanContext)
		return beanContext.addEvent( event.ProbeEvent().construct(self.executionTime(),
																  beanContext.star(self.star()),
																  beanContext.player(self.player()),
																  beanContext.player(self.star().owner()),
																  self.hasSpyShield(),
																  starInfo) )

	def execute(self):
		shield = self.star().hasSpyShield()
		self.setHasSpyShield(shield)
		if not shield:
			self.setWealth( self.star().wealth() )
			self.setNumShips( self.star().numShips() )
			self.setNumFactories( self.star().numFactories() )
			self.setHasDeathShield( self.star().hasDeathShield() )
