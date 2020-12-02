
from mx import DateTime

class Game:
	"""
	External representation of the Game. All players get the same Game bean, there is no hidden information
	date/times are represented using the mx.DateTime package

	If timeCompression = 1, then each turn takes one day. timeCompression = 2 implies that each turn takes 1/2 day and
	ships fly twice as fast. And so forth.
	"""
	def __init__(self):
		self._id = None
		self._startTime = None
		self._endTime = None
		self._currentTime = None
		self._nextProductionTime = None
		self._novaBombCost = None
		self._probeCost = None
		self._factoryCost = None
		self._speedCost = None
		self._rangeCost = None
		self._probeShieldCost = None
		self._novaShieldCost = None
		self._timeCompression = None
	
	def construct(self, id, startTime, endTime, currentTime, nextProductionTime, novaBombCost,
				 probeCost, factoryCost, speedCost, rangeCost, probeShieldCost, novaShieldCost, timeCompression):
		self._id = id
		self._startTime = startTime
		self._endTime = endTime
		self._currentTime = currentTime
		self._nextProductionTime = nextProductionTime
		self._novaBombCost = novaBombCost
		self._probeCost = probeCost
		self._factoryCost = factoryCost
		self._speedCost = speedCost
		self._rangeCost = rangeCost
		self._probeShieldCost = probeShieldCost
		self._novaShieldCost = novaShieldCost
		self._timeCompression = timeCompression
		return self

	def id(self): return self._id
	def startTime(self): return self._startTime
	def endTime(self): return self._endTime
	def currentTime(self): return self._currentTime
	def nextProductionTime(self): return self._nextProductionTime
	def novaBombCost(self): return self._novaBombCost
	def probeCost(self): return self._probeCost
	def factoryCost(self): return self._factoryCost
	def speedCost(self): return self._speedCost
	def rangeCost(self): return self._rangeCost
	def probeShieldCost(self): return self._probeShieldCost
	def novaShieldCost(self): return self._novaShieldCost
	def timeCompression(self): return self._timeCompression

	def __str__(self):
		return "Game %s at %s [ start : %s, end : %s ]" % ( self.id(), self.currentTime(), self.startTime(), self.endTime() )

