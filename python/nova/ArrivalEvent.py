'''
ArrivalEvent.py
'''

from nova.util import Log

from nova.Exceptions import InvalidEventException
from nova.FieryDeathEvent import FieryDeathEvent
from nova.BattleEvent import BattleEvent
import nova
from nova.bean import event

from GeneratedPy.GenArrivalEvent import GenArrivalEvent

from mx import DateTime

class ArrivalEvent(GenArrivalEvent):
	def __init__(self):
		GenArrivalEvent.__init__(self)
		self._abort = 0

	def createBean(self, beanContext):
		"""
		Construct an ArrivalEvent bean for this ArrivalEvent
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		departure = self.departureEvent()
		return beanContext.addEvent( event.ArrivalEvent().construct(self.executionTime(),
																	beanContext.star(departure.destination()),
																	beanContext.star(departure.finalDestination()),
																	beanContext.star(departure.origin()),
																	departure.numShips()) )
		
	def execute(self):
		"""
		If the destination star is dead, create a new FieryDeathEvent
		Else, if the destination star is owned by the player that sent the fleet, add the ships to the
		destination star.
		Else, create a new Battle
		"""
		departure = self.departureEvent()
		
		if departure.destination().isDead():
			Log.log(departure.numShips(), ' dying a fiery death at ', departure.destination().name())
			self._abort = 1
			death = FieryDeathEvent()
			death.construct(self.game(), self.executionTime(), self.player(), self.departureEvent())
			return [ death ]
		elif departure.destination().owner() is self.player():
			Log.log(departure.numShips(), ' arriving at ', departure.destination().name())
			departure.destination().addShips( departure.numShips() )
			if departure.finalDestination() is not None and departure.destination() is not departure.finalDestination():
				# Route the ships to the next star in the path towards their final destination
				Log.log('Fleet continuing to ', departure.finalDestination().name())
				newDeparture = nova.DepartureEvent.DepartureEvent()
				newDeparture.construct(self.game(), DateTime.now(), self.player(), departure.numShips(),
					departure.destination(), departure.finalDestination(), 'Ship')
				return [ newDeparture ]
			else:
				return []
		else:
			self._abort = 1
			battle = BattleEvent()
			Log.log(departure.numShips(), ' going into battle at ', departure.destination().name())
			battle.construct(self.game(), self.executionTime(), departure.player(), departure.destination(),
								  self.player(), departure.destination().owner(), departure.numShips())
			return [ battle ]

	def aborted(self):
		return self._abort
