'''
FieryDeathEvent.py
'''

from nova.util import Log
from nova.bean import event

from GeneratedPy.GenFieryDeathEvent import GenFieryDeathEvent

class FieryDeathEvent(GenFieryDeathEvent):
	def createBean(self, beanContext):
		"""
		Construct an FieryDeathEvent bean
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		departure = self.departureEvent()
		return beanContext.addEvent( event.FieryDeathEvent().construct(self.executionTime(),
																	   beanContext.star(departure.destination()),
																	   departure.numShips()) )

	def execute(self):
		# The ships just go away...
		pass
