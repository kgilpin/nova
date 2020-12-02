import types

from nova.trigger import trigger
from nova.engine import store

from nova.ArrivalEvent import ArrivalEvent
from nova.BattleEvent import BattleEvent
from nova.DeathProbeEvent import DeathProbeEvent
from nova.DepartureEvent import DepartureEvent
from nova.ProductionEvent import ProductionEvent
from nova.Star import Star

from mx import DateTime

class AutoDeployTrigger(trigger.Trigger):
	"""
	Trigger which automatically dispatches ships from an origin star to a destination. The origin
	can be garrisoned with a specified number of ships.
	"""
	
	def __init__(self):
		self._origin = None
		self._garrison = None
		self._destination = None

	def userFields(self):
		return [ ( 'origin', types.LongType, None ), ( 'destination', types.LongType, None ),
			( 'garrison', types.IntType, 0 ) ]

	def setOrigin(self, origin): 
		"Origin star from which ships will be sent"
		self._setStar('origin', origin)
		assert self._origin is not None
				
	def setGarrison(self, garrison): 
		" The garrison is the number of ships that will always be left to defend the "
		self._garrison = garrison
		
	def setDestination(self, destination): 
		"Destination star to which ships will be sent"
		self._setStar('destination', destination)
		assert self._destination is not None

	def triggerType(self):
		"This class is an Event trigger"
		return trigger.TRIGGER_TYPE_EVENT

	def cancel(self, event, player):
		"""
		The trigger is canceled if the player loses the origin star or destination star to a BattleEvent
		or DeathProbeEvent
		"""
		if isinstance(event, BattleEvent):
			if ( event.star() is self._origin or event.star() is self._destination ) and event.victor() is not player:
				return 1
		if isinstance(event, DeathProbeEvent):
			if ( event.star() is self._origin or event.star() is self._destination ) and not event.hasDeathShield():
				return 1
		return 0
			
	def applyTo(self, event, player):
		"""
		Applied when a ProductionEvent for the origin star occurs, or an ArrivalEvent occurs
		whose destination is the origin star
		"""
		if isinstance(event, ProductionEvent) and event.star() is self._origin:
			return 1
		if isinstance(event, ArrivalEvent):
			departure = event.departureEvent()
			if departure.destination() is self._origin:
				return 1
		return 0

	def newEvents(self, event, player):
		"""
		Sends all available ships (minus the garrison) from the origin to the destination
		"""
		numShips = self._origin.numShips() - self._garrison
		if numShips > 0:
			newDeparture = DepartureEvent()
			newDeparture.construct(event.game(), DateTime.now(), player, numShips,
				self._origin, self._destination, 'Ship')
			return [ newDeparture ]			
		else:
			return []

	def _setStar(self, attrName, value):
		if isinstance(value, Star):
			setattr(self, '_%s' % attrName, value)
		elif isinstance(value, types.LongType):
			setattr(self, '_%s' % attrName, store.get().fetchObject(Star, value))
		else:
			raise "Invalid argument type for '%s=%s' : %s. Expected Star or IntType" % ( attrName, value, type(value) )

	def __repr__(self):
		return "Deploy from %s to %s, garrison %d" % ( self._origin.name(), self._destination.name(), self._garrison )			
