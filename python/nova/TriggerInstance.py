'''
TriggerInstance.py
'''

import cPickle

from GeneratedPy.GenTriggerInstance import GenTriggerInstance

class TriggerInstance(GenTriggerInstance):

	def __init__(self):
		GenTriggerInstance.__init__(self)

	def getUserFieldsMap(self):
		"""
		Parses out a list of name/value pairs from the userFieldValues property
		"""
		userFields = cPickle.loads(self.userFieldValues())
		result = { }
		for name, value in userFields:
			result[name] = value
		return result
		
	def setUserFieldsAsMap(self, map):
		self.setUserFieldValues(cPickle.dumps(map))
		