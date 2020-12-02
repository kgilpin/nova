'''
DepartureEvent.py
'''

import log4py

from nova.Exceptions import InvalidEventException
from nova.ArrivalEvent import ArrivalEvent
from nova.DeathProbeEvent import DeathProbeEvent
from nova.SpyProbeEvent import SpyProbeEvent
from nova.Star import Star
# TODO: move to a different package, like engine
from nova.trigger import dijkstra
from nova.bean import fleet

from GeneratedPy.GenDepartureEvent import GenDepartureEvent

from mx import DateTime

Log = None

def travelTime(origin, destination, player, unitType):
	# DateTimeDelta is expressed in Days, Hours
	travelTime = DateTime.DateTimeDelta(0, origin.distanceTo(destination) / player.speed()) / \
					 player.game().timeCompression()
	if unitType == 'DeathProbe' or unitType == 'SpyProbe':
		travelTime /= 2
	return travelTime	

def buildStarGraph(stars, maxRange):
	"""
	Build a graph G suitable for the Dijkstra algorithm from a list of Stars and a player
	maximum range
	"""
	G = {}
	for first in stars:
		G[first] = {}
		for second in stars:
			if second is not first:
				distance = first.distanceTo(second)
				if distance <= maxRange:
					G[first][second] = distance
	return G

def nextStarInPath(store, player, origin, destination):
	stars = store.fetchObjectsOfClass(Star, clauses="WHERE ownerId = %s" % ( player.sqlObjRef() ))
	if not origin in stars:
		stars.append(origin)
	if not destination in stars:
		stars.append(destination)
	Log.debug('Routing ships from %s to %s for %s (range=%d)' % ( origin, destination, player, player.range() ) )
	graph = buildStarGraph(stars, player.range())
	try:
		path = dijkstra.shortestPath(graph, origin, destination)
	except KeyError, x:
		# print "Exception : ", x
		# This error indicates there is no such path
		return None
	return path[1]

class DepartureEvent(GenDepartureEvent):
	def construct(self, game, executionTime, player, numShips, origin, destination, unitType):
		"""
		Construct a DepartureEvent with an origin and a destination. The destination does not need to be 
		in range of the origin star if the unitType is 'Ship', and if there is some path along owned stars
		that reaches from origin to destination.
		"""
		nextStar = None
		if unitType == 'Ship':
			nextStar = nextStarInPath(game.store(), player, origin, destination)
		if nextStar is not None:
			Log.debug('Routing fleet through %s to %s' % ( nextStar, destination ))
			GenDepartureEvent.construct(self, game, executionTime, player, numShips, origin, nextStar, unitType)
			self.setFinalDestination(destination)
		else:
			Log.debug('Sending fleet directly to %s' % destination)
			GenDepartureEvent.construct(self, game, executionTime, player, numShips, origin, destination, unitType)
			
		self.setArrivalTime(self.computeArrivalTime())

	def createBean(self, beanContext):
		"""
		Construct a Fleet bean
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		ownerInfo = None
		if self.player() is beanContext.client():
			delayMinutes = self.executionTime() - beanContext.currentTime()
			if delayMinutes < 0:
				delayMinutes = 0
			ownerInfo = fleet.FleetOwnerInfo().construct(beanContext.star(self.finalDestination()), delayMinutes)
		if self.unitType() == 'Ship':
			unitType = 'Ship'
		elif self.unitType() == 'SpyProbe':
			unitType = 'Probe'
		else:
			unitType = 'NovaBomb'
		return fleet.Fleet().construct(self.serialNum(), beanContext.player(self.player()), beanContext.star(self.origin()),
									   beanContext.star(self.destination()), self.numShips(), self.executionTime(),
									   self.arrivalTime(), unitType, ownerInfo)
		
	def validate(self):
		"""
		Verify that the game will not be over by the time the units arrive
		Verify that the origin and destination are different
		Verify that the star of origin has enough ships, is not dead
		Verify that the player owns the origin star
		Verify that the player has enough range
		Verify that the player can afford the new unit
		"""
		if self.arrivalTime() > self.game().endTime():
			raise InvalidEventException('There is not enough time left in the game')
		if self.origin().isDead() or self.destination().isDead():
			raise InvalidEventException('Star %s is dead!' % self.origin().name())
		
		if self.origin() is self.destination():
			raise InvalidEventException('The origin and destination must be different')
		
		if self.unitType() == 'Ship':
			if self.origin().numAvailableShips() < self.numShips():
				raise InvalidEventException('Star %s (%d ships) does not have %d ships to send' %
													 ( self.origin().name(), self.origin().numAvailableShips(), self.numShips() ) )
			if self.numShips() <= 0:
				raise InvalidEventException('You must send at least 1 ship')
				
		if self.unitType() == 'DeathProbe':
			self.validateCost(self.game().deathProbeCost(), "a Death Probe")
		if self.unitType() == 'SpyProbe':
			self.validateCost(self.game().spyProbeCost(), "a Spy Probe")

		if self.player() is not self.origin().owner():
			raise InvalidEventException("You do not own star %s" % ( self.destination().name() ) )
		if self.player().range() < self.origin().distanceTo(self.destination()):
			raise InvalidEventException("Not enough range to get from %s to %s. Range is %f, distance is %f" %
												 ( self.origin().name(), self.destination().name(),
												   self.player().range(), self.origin().distanceTo(self.destination()) ) )

	def execute(self):
		"""
		Remove the ships from the origin star and create a new ArrivalEvent, DeathProbeEvent, or SpyProbeEvent
		"""
		if self.unitType() == 'Ship':
			self.origin().subtractShips( self.numShips() )
			Log.debug('Sent %d ships from %s to %s' % ( self.numShips(), self.origin().name(), self.destination().name() ) )
			arrival = ArrivalEvent()
			arrival.construct( self.game(), self.arrivalTime(), self.player(), self )
			return [ arrival ]
		elif self.unitType() == 'DeathProbe':
			Log.debug('Sent DeathProbe from %s to %s' % ( self.origin().name(), self.destination().name() ) )
			self.player().subtractWealth(self.game().deathProbeCost())
			dp = DeathProbeEvent()
			dp.construct( self.game(), self.arrivalTime(), self.player(), self.destination() )
			return [ dp ]
		elif self.unitType() == 'SpyProbe':
			Log.debug('Sent SpyProbe from %s to %s' % ( self.origin().name(), self.destination().name() ))
			self.player().subtractWealth(self.game().spyProbeCost())
			sp = SpyProbeEvent()
			sp.construct( self.game(), self.arrivalTime(), self.player(), self.destination(), self.destination().owner() )
			return [ sp ]
		else:
			raise "Invalid unitType %s" % self.unitType()
		
	def computeArrivalTime(self):
		tt = travelTime(self.origin(), self.destination(), self.player(), self.unitType())
		return self.executionTime() + tt

Log = log4py.Logger().get_instance(DepartureEvent)
			
