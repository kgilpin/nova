import types

from WebKit.XMLRPCServlet import XMLRPCServlet

from nova.engine import store
from nova.api import dispatch, exception, query
from nova.xmlrpc import Marshal
from nova.Game import Game
from mx import DateTime

class XMLRPCAPI(XMLRPCServlet):
	"""
	XML-RPC API for Nova.  To try it out, use something like the following:

	>>> import xmlrpclib
	>>> server = xmlrpclib.Server('http://localhost/cgi-bin/OneShot.cgi/Nova/XMLRPCAPI.py')
	>>> server.dispatchFleet(1, 'joebob', 'passwd', 'Orion', 'Sirius', 10, 0)
	1

	This logs in joebob and immediately sends 10 ships from Orion to Sirius.
	"""
	
	def exposedMethods(self):
		return [ 'dispatchFleet', 'dispatchProbe', 'dispatchNovaBomb', 'getSnapshot' ]

	def getSnapshot(self, *args):
		"""
		arguments : gameId, playerName, password, eventTurns
	
		eventTurns : how many turns worth of events to include in the snapshot. May be 0
		"""
		gameId, playerName, password, eventTurns = list(args)
		game = store.get().fetchObjectsOfClass(Game, serialNum=gameId)[0]
	
		delayDays = 1 / game.timeCompression()
		since = DateTime.now() - DateTime.DateTimeDelta(delayDays)
		# getSnapshot authenticates the player from gameId, playerName, password
		return self.executeCommand(query.getSnapshot, ( game, playerName, password ), since )
		
	def dispatchFleet(self, *args):
		""" args: credentials, origin, destination, numShips, delay """
		return self.dispatch(dispatch.DispatchFleet, *args)

	def dispatchNovaBomb(self, *args):
		""" args: credentials, origin, destination, delay """
		return self.dispatch(dispatch.DispatchDeathProbe, *args)

	def dispatchProbe(self, *args):
		""" args: credentials, origin, destination, delay """
		return self.dispatch(dispatch.DispatchSpyProbe, *args)

	def dispatch(self, cls, *args):
		# See if the optional arguments are specified
		args = list(args)
		delay = int(args.pop())
		instance = cls()
		if delay > 0:
			# print 'Setting delay = %d' % delay
			instance.setDelayMinutes(delay)
		return self.executeCommand(instance.execute, *args)

	def executeCommand(self, command, *args):
		try:
			result = command(*args)
			if result is None:
				return { 'succeeded' : 1 }				
			elif isinstance(result, types.InstanceType):
				resultMap = Marshal.Marshal().marshal(result)
				return { 'succeeded' : 1, 'result' : resultMap }
			else:
				return { 'succeeded' : 1, 'result' : result }
		except exception.APIException, x:
			return { 'succeeded' : 0, 'errorMessage' : str(x) }
		except:
			import traceback, sys
			type, value, tb = sys.exc_info()
			lines = traceback.format_exception(type, value, tb)
			return { 'succeeded': 0, 'errorMessage' : '\n'.join(lines) }
