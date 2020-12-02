import cPickle, traceback, sys, string

import nova.trigger.battleMessage
import nova.trigger.deploy

from nova.util import Log

class TriggerProcessor:
	"""
	Processes a trigger. The basic procedure is
		instantiate the trigger object from its class name
		load the user fields and set the corresponding attributes on the class instance
		for each event
			if the trigger should be applied to that event:
				send the trigger message or create the new trigger events
	"""
	def __init__(self, transportMap):
		"""
		tranportMap is a map from transport name (e.g. 'Email') to nova.trigger.transport.Transport objects.
		'Email' must be one of the keys
		"""
		self._transportMap = transportMap
		
	def processEvents(self, triggerInstance, events, newEvents):
		"""
		Events created by the trigger are added to the newEvents list. Messages are sent using
		the corresponding transport
		"""

		Log.debug('TriggerProcessor processing %s' % triggerInstance)
		
		triggerDef = triggerInstance.triggerDef()
		try:
			trigger = eval('%s()' % triggerDef.className())
			if triggerInstance.userFieldValues() is not None:
				fields = triggerInstance.getUserFieldsMap()
				for name, value in fields.items():
					method = getattr(trigger, 'set%s' % string.capitalize(name))
					Log.debug('Setting trigger field %s=%s' % ( name, value ))
					method(value)
		except Exception, x:
			#import traceback
			#traceback.print_exc()
			self.mailException(triggerInstance)
			return
				
		for event in events:
			Log.debug('TriggerProcessor processing %s' % event)
			try:		
				if trigger.cancel(event, triggerInstance.player()):
					Log.debug('Canceling %s' % triggerInstance)
					triggerInstance.store().deleteObject(triggerInstance)
				else:
					if trigger.applyTo(event, triggerInstance.player()):
						Log.debug('Applying %s' % triggerInstance)
						if trigger.triggerType() == nova.trigger.trigger.TRIGGER_TYPE_MESSAGE:
							message = trigger.message(event, triggerInstance.player())
							self._transportMap[triggerInstance.messageTransport()].sendMessage(triggerInstance.player(),
								message)
							Log.debug('Trigger %s sent message %s' % ( trigger, message ))
						elif trigger.triggerType() == nova.trigger.trigger.TRIGGER_TYPE_EVENT:
							triggerEvents = trigger.newEvents(event, triggerInstance.player())
							if len(triggerEvents):
								Log.debug('Trigger %s created new events %s' % ( trigger, triggerEvents ))
							newEvents.extend( triggerEvents )
						else:
							raise Exception, "Unexpected Trigger type : %s" % trigger.triggerType()
			except:
				#import traceback
				#traceback.print_exc()
				self.mailException(triggerInstance)
				
	def mailException(self, triggerInstance):
		type, value, tb = sys.exc_info()
		exceptionMessage = traceback.format_exception(type, value, tb)
		self._transportMap['Email'].sendMessage(triggerInstance.player(),
			nova.trigger.trigger.Message('Exception in trigger %s' % triggerInstance.triggerDef().className(), ''.join(exceptionMessage)))

