import types

from nova.Event import Event
from nova.Game import Game
from nova.Exceptions import InvalidEventException
from nova.TriggerInstance import TriggerInstance
from nova.trigger.transport import EmailTransport

from nova.engine import triggerProcessor

from nova.util import Log

from MiddleKit.Run.MySQLObjectStore import MySQLObjectStore
from mx import DateTime

class Engine:
	def __init__(self, store):
		self.store = store
		self._transports = {}
	
	def setTransport(self, name, transport):
		"""
		Specify that a specific transport object should be used for the named transport
		Typical usage is to replace a transport such as 'Email' with a test stub
		"""
		self._transports[name] = transport
	
	def tick(self):
		games = self.store.fetchObjectsOfClass(Game)
		for game in games:
			self.doSavedEvents(game)

	def doSavedEvents(self, game):
		"""
		Process all the events for a particular game which are saved in the database and scheduled to execute
		"""
		# Fetch all events which should be executed, grabbing the earliest ones first
		# Do the first one, or return if there are none
		events = self.store.fetchObjectsOfClass(Event, clauses="WHERE gameId = %s AND status = 'Pending' " \
																 "AND executionTime <= NOW() " \
																 "ORDER BY executionTime ASC" % game.sqlObjRef())
		Log.debug("Fetched events ", events, " from database")
		if len(events):
			return self.execute(events)
		else:
			return {}

	def execute(self, events):
		"""
		Fully execute a game event or events.
		Return a tuple of ( event, errorMessage ) if the event, or an event that it spawns, cannot be executed.
		"""
		if type(events) is not types.ListType:
			events = [ events ]

		if not len(events):
			return {}
		
		errors = {}

		for event in events:
			if event.executionTime() > event.game().endTime():
				errors[event] = 'The game is over!'
				events.remove(event)
				event.setStatus( 'Aborted' )
			self.store.addObject(event)
		
		self.sortByExecutionTime(events)
		
		conn = self.lock()	
		try:
			while len(events) and events[0].executionTime() <= DateTime.now():	
				event = events.pop(0)
				newEvents = self.processEvent(event, errors)
				events.extend(newEvents)
				if not event in errors.keys() and not event.aborted():
					events.extend( self.processTriggers([ event ]) )
				
				self.sortByExecutionTime(events)
		finally:
			self.store.saveChanges()
			self.unlock(conn)
			conn.close()
			
		Log.debug("Returning error map ", errors)
		return errors
	
	def abort(self, event):
		"""
		Sets the status of an event to 'Aborted' if the event is in the Pending state.
		Returns an empty map if the event was aborted. Otherwise, a map from the event to an error message
		
		This is a top-level function. It should not be invoked by the Engine internally because it calls
		lock(), which frees any existing lock and acquires a new one
		"""
		conn = self.lock()
		errors = {}
		try:
			if event.status() == 'Pending':
				event.setStatus( 'Aborted' )
			else:
				errors[event] = 'Unable to abort event. Event status is %s' % event.status()
		finally:
			self.store.saveChanges()
			self.unlock(conn)
		return errors

	def processEvents(self, events, errors={}):
		"""
		This method is just a hook for the test harness
		"""
		newEvents = []
		for event in events:
			newEvents[len(newEvents):] = self.processEvent(event, errors)
		return newEvents

	def processEvent(self, event, errors={}):
		"""
		Process a single event, returning a list of new events that it creates.
		Error messages are placed in the errors list, keyed by the event
		"""
		game = event.game()
		eventCounter = game.eventCounter()

		Log.debug("processing event ", event)

		newEvents = []

		if event.executionTime() > event.game().endTime():
			errors[event] = "The game is over!"
			return newEvents

		# So we can see which ones are being executed
		self.store.addObject(event)
		event.setStatus('InProcess')
		self.store.saveChanges()

		try:
			event.validate()
			newEvents = event.execute()
			if newEvents is not None:
				Log.debug(event, ' created new events ', newEvents)
			else:
				newEvents = []
				
			if event.aborted():
				event.setStatus( 'Aborted' )
			else:
				event.setStatus( 'Complete' )
		except InvalidEventException, x:
			Log.warn('InvalidEvent : ', x)
			event.setStatus( 'Invalid' )
			errors[event] = str(x)
		except Exception, x:
			import traceback
			traceback.print_exc()
			Log.warn(x.__class__, ' : ', x)
			event.setStatus( 'Invalid' )
			errors[event] = str(x)
			
		event.setEventCounter( eventCounter )
		eventCounter += 1
		game.setEventCounter(eventCounter)

		for newEvent in newEvents:
			Log.debug('Adding new event : ', newEvent)
			self.store.addObject(newEvent)

		event.game().setLastActionTime(event.executionTime())

		self.store.saveChanges()
			
		return newEvents

	def processTriggers(self, events):
		"""
		Load and evaluate all the triggers that apply to the just-completed event
		Return the new events that are created by the triggers
		"""
		if not len(events):
			return []

		transports = self._transports.copy()
		if not transports.has_key('Email'):
			transports['Email'] = EmailTransport()
			
		processor = triggerProcessor.TriggerProcessor(transports)
		triggers = self.store.fetchObjectsOfClass(TriggerInstance, "WHERE gameId = %s" % events[0].game().sqlObjRef())
		newEvents = []
		for trigger in triggers:
			Log.debug('Processing trigger %s' % trigger)
			processor.processEvents(trigger, events, newEvents)
		if len(newEvents):
			Log.debug('Triggers created new events %s' % newEvents)
		return newEvents

	def lock(self):
		conn, cur = self.store.executeSQL("LOCK TABLES GlobalLock WRITE;")
		cur.close()
		return conn

	def unlock(self, conn):
		self.store.executeSQL("UNLOCK TABLES;", conn)

	def sortByExecutionTime(self, events):
		# Sort all the events by their executionTime
		events.sort(lambda first, second: int( ( first.executionTime() - second.executionTime() ).seconds ) )
		Log.debug("Sorted list of events is ", events)

if __name__ == "__main__":
	from nova.engine import store
	from nova.trigger.transport import DummyTransport
	
	#Log.enabled = 1
	print 'Running Nova engine at %s' % DateTime.now()
	engine = Engine(store.get())
	#dummy = DummyTransport()
	#engine.setTransport('Email', dummy)
	engine.tick()
	#print dummy
