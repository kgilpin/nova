'''
Event.py
'''


from nova.Exceptions import InvalidEventException
from nova.util import Log 
from nova.beanContext import BeanContext

from GeneratedPy.GenEvent import GenEvent

class Event(GenEvent):

	def __init__(self):
		GenEvent.__init__(self)

	def __str__(self):
		if hasattr(self, 'createBean'):
			bc = BeanContext(self.player())
			return str(self.createBean(bc))
		else:
			return "%s <%d>" % ( type(self), id(self) )

	def uiDescription(self, client):
		"""
		Return a formatted string which is displayed in the UI list of events
		The 'client' argument may be used to determine how much information should be presented
		in the description.
		The string may be formatted using HTML-like tags:
		<i>italics</i>
		<b>bold</b>
		<color>colorized text</color>
		<br/> : line break
		<unit qty=5 /> : specified number of ships
		<star name=Jazz /> : a star

		The description is empty by default, it is needed on events which are shown in the UI
		"""
		if hasattr(self, 'createBean'):
			bc = BeanContext(client)
			return self.createBean(bc).uiDescription()
		else:
			raise Exception, "No description of %s for player %s" % ( self, player.name() )

	def validate(self):
		"""
		Should raise an Exceptions.InvalidEventException if the Event should not be allowed to be processed
		"""
		pass

	def execute(self):
		Log.log("Executing %s" % self)

	def aborted(self):
		"""
		Return 1 if the event has been aborted and processing of it should not continue.
		"""
		return 0

	def validateCost(self, cost, itemDescription):
		"""
		Should raise an Exceptions.InvalidEventException if the Event should not be allowed to be processed
		because the player cannot afford it
		"""
		if self.player().availableCash() < cost:
			raise InvalidEventException('Player %s cannot afford $%s for %s' % ( self.player().name(), cost, itemDescription ) )

	def validateOwner(self, star):
		"""
		Should raise an Exceptions.InvalidEventException if the Event should not be allowed to be processed
		because the player does not own the star in question
		"""
		if self.player() is not star.owner():
			raise InvalidEventException('Player %s does not own %s' % ( self.player().name(), star.name() ) )


