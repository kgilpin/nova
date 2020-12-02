import types
import log4py
from mx import DateTime

import method

from nova.ArrivalEvent import ArrivalEvent
from nova.DepartureEvent import DepartureEvent
from nova.Star import Star
from nova.engine import store

Log = None

class Dispatch(method.APIMethod):
	def __init__(self):
		self._delay = 0
		
	def setDelayMinutes(self, delay):
		self._delay = delay

	def _execute(self, gameId, playerName, password, origin, destination, unitType, numShips):
		"""
		Return a map from game events (actions) to failure error messages.
		"""
		game = self.game(gameId)
		player = self.login(game, playerName, password)

		originStar = self._findStar(game, "Origin", origin)
		destinationStar = self._findStar(game, "Destination", destination)
													 										 
		departure = DepartureEvent()
		departure.construct(game, DateTime.now() + DateTime.DateTimeDelta(0, 0, self._delay), \
							player, numShips, originStar, destinationStar, unitType)
		try:
			departure.validate()
		except Exception, x:
			# The event should never be saved in the DB since we are not going to give it to the engine
			departure.setStatus('Invalid')
			return { departure : str(x) }

		return self.executeEvent(departure)

	def _findStar(self, game, whichStar, starId):
		""" Find a star identified either by a name or by an id """
		if isinstance(starId, types.StringType):
			return self.findObject(Star, "WHERE gameId = %s AND name = '%s'" % ( game.sqlObjRef(), starId ),
												  "%s star %s not found" % ( whichStar, starId ) )
		else:
			return self.findObject(Star, "WHERE starId = %s" % starId, "%s star %s not found" % ( whichStar, starId ) )

class DispatchFleet(Dispatch):
	def execute(self, gameId, playerName, password, origin, destination, numShips):
		"""
		Send numShips ships from origin to destination
		"""
		return Dispatch._execute(self, gameId, playerName, password, origin, destination, 'Ship', numShips)

class DispatchDeathProbe(Dispatch):
	def execute(self, gameId, playerName, password, origin, destination):
		"""
		Send a death probe from origin to destination
		"""
		return Dispatch._execute(self, gameId, playerName, password, origin, destination, 'DeathProbe', 1)

class DispatchSpyProbe(Dispatch):
	def execute(self, gameId, playerName, password, origin, destination):
		"""
		Send a spy probe from origin to destination
		"""
		return Dispatch._execute(self, gameId, playerName, password, origin, destination, 'SpyProbe', 1)

class Abort(method.APIMethod):
	def execute(self, gameId, playerName, password, departureId):
		"""
		Find the specified DepartureEvent and Abort it
		Either the DepartureEvent must have not started yet, or it must be a DepartureEvent with a non-empty
			finalDestination, and it must not have Arrived yet
		"""
		game = self.game(gameId)
		player = self.login(game, playerName, password)
		
		departure = self.findObject(DepartureEvent, "WHERE playerId = %s AND departureEventId = '%s'" % \
			( player.sqlObjRef(), departureId ), "Departure %d not found for player %s" % ( departureId, playerName ))
		
		errors = self.abortEvent(departure)
		if len(errors) and departure.finalDestination() is not None and departure.finalDestination() is not departure.destination():
			Log.debug('abortEvent failed. Looking for Pending ArrivalEvent for routed fleet')
			arrivals = store.get().fetchObjectsOfClass(ArrivalEvent, "WHERE departureEventId = %s AND status = 'Pending'" % departure.sqlObjRef())
			if len(arrivals):
				Log.debug('ArrivalEvent found. Setting finalDestination = destination')
				departure.setFinalDestination(departure.destination())
				store.get().saveChanges()
				return {}
		return errors
			
Log = log4py.Logger().get_instance(Dispatch)
		