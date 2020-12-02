from mx import DateTime

class Fleet:
	def construct(self, id, player, origin, destination, numShips, departureTime, arrivalTime, unitType, ownerInfo):
		"""
		unitType is one of ( 'Ship', 'Probe', 'NovaBomb' )
		"""
		self._id = id
		self._player = player
		self._origin = origin
		self._destination = destination
		self._numShips = numShips
		self._departureTime = departureTime
		self._arrivalTime = arrivalTime
		self._unitType = unitType
		self._ownerInfo = ownerInfo
		if ownerInfo:
			ownerInfo._fleet = self
		return self

	def id(self): return self._id
	def player(self): return self._player
	def origin(self): return self._origin
	def destination(self): return self._destination
	def numShips(self): return self._numShips
	def departureTime(self): return self._departureTime
	def arrivalTime(self): return self._arrivalTime
	def unitType(self): return self._unitType
	def ownerInfo(self): return self._ownerInfo

	def isPending(self, game):
		return self.departureTime() > game.currentTime()

	def percentTraveled(self):
		"""
		Return the percentage of the journey that has been made so far
		"""
		totalTravelTime = self.arrivalTime() - self.departureTime();
		currentTravelTime = DateTime.now() - self.departureTime();
		percent = 0
		if totalTravelTime != 0:
			percent = currentTravelTime / totalTravelTime * 100.0;
		if percent > 100:
			percent = 100
		if percent < 0:
			percent = 0
		return percent

	def __str__(self):
		return "[%s] %s sending %d %s from %s to %s" % ( self.departureTime(), self.player().name(), self.numShips(), self.unitType(), \
													self.origin().name(), self.destination().name() )
		
class FleetOwnerInfo:
	def construct(self, finalDestination, delayMinutes):
		"""
		delayMinutes is an integer greater than zero if the departureTime is in the future (relative to the Game.currentTime)
		"""
		self._finalDestination = finalDestination
		self._delayMinutes = delayMinutes
		self._fleet = None
		return self

	def finalDestination(self): return self._finalDestination
	def delayMinutes(self): return self._delayMinutes
	def fleet(self): return self._fleet
	
