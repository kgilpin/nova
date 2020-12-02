import os
import unittest

from MiscUtils.Configurable import Configurable

from nova.User import User

class NovaTest(unittest.TestCase, Configurable):
	def __init__(self, name):
		unittest.TestCase.__init__(self, name)
		Configurable.__init__(self)
	
	def novaURL(self):
		return self.setting('NovaURL')

	def defaultConfig(self):
		return { }

	def configFilename(self):
		dir = os.path.dirname(__file__)
		return os.path.join(os.path.abspath(dir), 'Test.config')

	def makeUser(self, name, password, email):
		users = self.store.fetchObjectsOfClass(User, clauses="WHERE name = '%s'" % name)
		if not len(users):
			user = User()
			user.construct(name, password, email)
		else:
			user = users[0]
		return user