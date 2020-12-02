import sys, unittest, log4py

from test import connection

from nova.BattleEvent import BattleEvent
from nova.TriggerInstance import TriggerInstance
from nova.engine.triggerProcessor import TriggerProcessor
from nova.trigger.transport import EmailTransport

from nova.util import Log

class TestTriggerMail(unittest.TestCase):

	def setUp(self):
		self.store = connection.get()

	def testBattleMail(self):
		"""
		Load a BattleEvent and run it through an e-mail Battle trigger
		"""
		be = self.store.fetchObject(BattleEvent, 118)
		ti = self.store.fetchObject(TriggerInstance, 3)
		transports = { 'Email' : EmailTransport() }
		tp = TriggerProcessor(transports)
		newEvents = []
		tp.processEvents(ti, [ be ], newEvents)
		print newEvents
		

if __name__=='__main__':
	log4py.Logger.instance.set_loglevel(log4py.LOGLEVEL_DEBUG)
	Log.enabled = 1
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()

