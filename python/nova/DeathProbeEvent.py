'''
DeathProbeEvent.py
'''


from GeneratedPy.GenDeathProbeEvent import GenDeathProbeEvent
from nova.bean import event

class DeathProbeEvent(GenDeathProbeEvent):
	def createBean(self, beanContext):
		"""
		Construct an NovaBombEvent bean
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		return beanContext.addEvent( event.NovaBombEvent().construct(self.executionTime(), beanContext.star(self.star()), self.hasDeathShield()) )

	def execute(self):
		shield = self.star().hasDeathShield()
		self.setHasDeathShield(shield)
		if not shield:
			self.star().setOwner(self.game().nobody())
			self.star().setIsDead(1)
