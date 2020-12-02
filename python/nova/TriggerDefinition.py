'''
TriggerDefinition.py
'''

from nova.trigger.battleMessage import BattleMessageTrigger
from nova.GeneratedPy.GenTriggerDefinition import GenTriggerDefinition

def _addTrigger(store, trigger):
	"""
	Adds a TriggerDefinition if its className is not already in the database
	"""
	triggers = store.fetchObjectsOfClass(TriggerDefinition, clauses="WHERE className = '%s'" % trigger.className())
	if not len(triggers):
		store.addObject(trigger)
		store.saveChanges()
		return trigger
	else:
		return triggers[0]

def battleMessageTrigger(store):
	trigger = TriggerDefinition()
	trigger.construct('nova.trigger.battleMessage.BattleMessageTrigger')
	return _addTrigger(store, trigger)	

def autoDeployTrigger(store):
	trigger = TriggerDefinition()
	trigger.construct('nova.trigger.deploy.AutoDeployTrigger')
	return _addTrigger(store, trigger)	

def installDefaultTriggers(store):
	"""
	Adds the default TriggerDefinitions to the data store
	Returns a list of them
	"""
	return [ battleMessageTrigger(store), autoDeployTrigger(store) ]
	
class TriggerDefinition(GenTriggerDefinition):
	def __init__(self):
		GenTriggerDefinition.__init__(self)
