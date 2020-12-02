import xmlrpclib
from nova.xmlrpc.Marshal import Marshal

class API:
	def __init__(self, novaURL, gameId, playerName, password):
		self.novaURL = novaURL
		self.server = xmlrpclib.Server('%s/XMLRPCAPI.py' % self.novaURL)
		self.loginInfo = ( gameId, playerName, password )
		
	def getSnapshot(self, eventTurns):
		args = self.loginInfo + ( eventTurns, )
		resultMap = self.server.getSnapshot(*args)
		ss = self._unmarshal(resultMap, "getSnapshot", args)
		assert ss is not None
		return ss

	def dispatchFleet(self, origin, destination, numShips, delayMinutes = 0):
		"""
		Dispatch a fleet
		origin, destination : nova.bean.Star objects
		delayMinutes : optional delay in minutes before the fleet is actually sent. Before this time expires, the fleet
			departure may be canceled
		"""
		args = self.loginInfo + ( origin.id(), destination.id(), numShips, delayMinutes )
		resultMap = self.server.dispatchFleet(*args)
		# This method returns None. An APIException is raised if the fleet cannot be dispatched
		self._unmarshal(resultMap, "dispatchFleet", args)

	def dispatchNovaBomb(self, origin, destination, delayMinutes = 0):
		"""
		Dispatch a Nova bomb
		origin, destination : nova.bean.Star objects
		delayMinutes : optional delay in minutes before the unit is actually sent. Before this time expires, the
			departure may be canceled
		"""
		args = self.loginInfo + ( origin.id(), destination.id(), delayMinutes )
		resultMap = self.server.dispatchNovaBomb(*args)
		# This method returns None. An APIException is raised if the unit cannot be dispatched
		self._unmarshal(resultMap, "dispatchNovaBomb", args)
		

	def dispatchProbe(self, origin, destination, delayMinutes = 0):
		"""
		Dispatch a probe
		origin, destination : nova.bean.Star objects
		delayMinutes : optional delay in minutes before the unit is actually sent. Before this time expires, the
			departure may be canceled
		"""
		args = self.loginInfo + ( origin.id(), destination.id(), delayMinutes )
		resultMap = self.server.dispatchProbe(*args)
		# This method returns None. An APIException is raised if the unit cannot be dispatched
		self._unmarshal(resultMap, "dispatchProbe", args)
		
	def _unmarshal(self, resultMap, methodName, args): 
		# print resultMap
		succeeded = resultMap['succeeded']
		if not succeeded:
			raise APIException(methodName, args, resultMap['errorMessage'])
		if resultMap.has_key('result') and resultMap['result']:
			return Marshal().unmarshal(resultMap['result'])
		else:
			return None

class APIException(Exception):
	def __init__(self, methodName, args, message):
		self.methodName = methodName
		self.args = args
		self.message = message
		
		# TODO: figure out the right way to invoke the superclass constructor
		Exception.__init__(self, self._message())
		
	def _message(self):
		return "Failed to invoke %s(%s). Error : %s" % ( self.methodName, self.args, self.message )
