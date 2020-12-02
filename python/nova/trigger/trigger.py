import re

TRIGGER_TYPE_MESSAGE	= 'Message'
TRIGGER_TYPE_EVENT		= 'Event'

class Message:
	"""
	Defines a trigger message
	"""
	def __init__(self, subject, body):
		self._subject = subject
		self._body = body

	def subject(self): return self._subject
	
	def body(self): return self._body
	
	def __repr__(self):
		return "%s\n%s" % ( self._subject, self._body )
		

class Trigger:
	"""
	Abstract base class which defines a Nova trigger. A trigger responds to a new game event
	by sending a message to a player, or by creating new events in response.
	"""
	
	def triggerType(self):
		"""
		Must be over-ridden to return TRIGGER_TYPE_MESSAGE or TRIGGER_TYPE_EVENT		
		"""
		raise NotImplementedError, self.__class__
		
	def cancel(self, event, player):
		"""
		Whether the event should cancel (delete) the trigger instance. This may occur if,
		for instance, the star for which the trigger is configured gets captured by the enemy
		or destroyed
		"""	
		return 0
		
	def applyTo(self, event, player):
		"""
		Must be overridden to return whether the trigger should be applied to this event.
		If this method returns true, either message() or newEvents() will be invoked, depending
		on triggerType()		
		"""
		raise NotImplementedError, self.__class__
		
	def userFields(self): 
		"""
		May return a list of ( name, type, defaultValue ) tuples for user customization fields.
		For each 'name', there should be a corresponding set<Name> method which will be invoked by the
		framework if the user supplies a value for the field.
		"""
		return []
		
	def message(self, event, player):
		"""
		If triggerType() is TRIGGER_TYPE_MESSAGE, this method should return a new Message object
		"""
		pass
		
	def newEvents(self, event, player):
		"""
		If triggerType() is TRIGGER_TYPE_EVENT, this method should return a list of new Events which
		will be sent to be processed by the Engine.
		"""
		pass
		