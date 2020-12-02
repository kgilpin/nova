import os
from MiddleKit.Run.MySQLObjectStore import MySQLObjectStore
from MiscUtils.Configurable import Configurable

class DBConfig(Configurable):
	def userName(self):
		return self.setting('DBUser')

	def password(self):
		return self.setting('DBPassword').strip()

	def defaultConfig(self):
		return { }

	def configFilename(self):
		dir = os.path.dirname(__file__)
		return os.path.join(os.path.abspath(dir), 'DB.config')

"""
Keeps a shared ObjectStore.

Without a shared instance, each new ObjectStore creates a bunch of connections and eventually
the connection limit of the server is exceeded
"""

_store = None

def get():
	global _store
	if _store is None:
		config = DBConfig()
		dir = os.path.dirname(__file__)
		modelFileName = os.path.join(os.path.abspath(dir), '..', 'Nova')
		try:
			_store = MySQLObjectStore(user=config.userName(), passwd=config.password())
			_store.readModelFileNamed(modelFileName)
		except Exception, x:
			try:
				_store = MySQLObjectStore(user=config.userName())
				_store.readModelFileNamed(modelFileName)
			except:
				raise x
	return _store
	
