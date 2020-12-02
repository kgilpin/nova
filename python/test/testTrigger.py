import unittest
import sys, traceback, time, cPickle

from basicGalaxy import BasicGalaxy
import testBattle
import nova

from nova.util import Log

from nova.api import dispatch
from nova.DepartureEvent import DepartureEvent
from nova.TriggerInstance import TriggerInstance
from nova.TriggerDefinition import TriggerDefinition, battleMessageTrigger, autoDeployTrigger
from nova.DeathProbeEvent import DeathProbeEvent
from nova.GlobalProductionEvent import GlobalProductionEvent
from nova.ProductionEvent import ProductionEvent

from nova.trigger.transport import DummyTransport
from nova.engine.triggerProcessor import TriggerProcessor

from mx import DateTime

class TestTrigger(BasicGalaxy):

	def testNoSuchClass(self):
		"""
		Tests an invalid trigger class name
		"""
		td = TriggerDefinition()
		td.construct('nova.such.cls')
		instance = TriggerInstance()
		instance.construct(td, self.kevin, 'Email', self.game)
		
		dummy = DummyTransport()
		transports = { 'Email' : dummy }
		processor = TriggerProcessor(transports)
		processor.processEvents(instance, [], [])
		
		self.assertEquals(1, len(dummy.messages))
		self.assertEquals(dummy.messages[0][0], self.kevin)
		self.assertEquals(dummy.messages[0][1].subject(), 'Exception in trigger nova.such.cls')
		self.assertNotEquals(dummy.messages[0][1].body(), dummy.messages[0][1].body().find("'nova' module has no attribute 'such'"), -1)
		self.assertNotEquals(dummy.messages[0][1].body(), dummy.messages[0][1].body().find('\n'), -1)

	def testExceptionInTrigger(self):
		"""
		Raises an exception in the applyTo method because Trigger is abstract
		"""
		td = TriggerDefinition()
		td.construct('nova.trigger.trigger.Trigger')
		instance = TriggerInstance()
		instance.construct(td, self.kevin, 'Email', self.game)
		
		departure = DepartureEvent()
		departure.construct(self.game, DateTime.now(), self.kevin, 20, self.corprl, self.klegg, 'Ship')
		
		dummy = DummyTransport()
		transports = { 'Email' : dummy }
		processor = TriggerProcessor(transports)
		processor.processEvents(instance, [ departure ], [])
		
		self.assertNotEquals(dummy.messages[0][1].body().find("NotImplementedError: nova.trigger.trigger.Trigger"), -1)

	def testDeploy(self):
		"""
		Deploy ships from Corporal to Klegg
		Run a ProductionEvent on Corporal
		Process the Deploy trigger with the ProductionEvent 
		Should create a new DepartureEvent that sends ships from Corporal to Klegg
		"""
		deploy = TriggerInstance()
		deploy.construct(autoDeployTrigger(self.store), self.kevin, 'Email', self.game)
		fields = [ 	( 'origin', self.corprl.serialNum() ),
					( 'destination', self.klegg.serialNum() ),
					( 'garrison', 10 ) ]
		deploy.setUserFieldValues(cPickle.dumps(fields))
		self.store.saveChanges()

		gp = GlobalProductionEvent()
		gp.construct(self.game, DateTime.now())
		self.store.addObject(gp)
		production = ProductionEvent()
		production.construct(self.game, DateTime.now(), self.kevin, self.corprl, 0, 0, gp)
		self.store.addObject(production)
		
		self.processEvents([ production ])

		processor, dummy = self.makeTriggerProcessor()
		newEvents = []
		processor.processEvents(deploy, [ production ], newEvents)

		self.assertEquals(0, len(dummy.messages), dummy.messages)
		
		self.assertEquals(1, len(newEvents))
		departure = newEvents[0]
		self.failUnless(isinstance(departure, DepartureEvent))
		self.assertEquals(self.corprl, departure.origin())
		self.assertEquals(self.klegg, departure.destination())
		# Should send all but 10 of the 200 ships
		self.assertEquals(190, departure.numShips())
		
	def testCancelDeploy(self):
		"""
		Deploy ships from Corporal to Klegg
		Blow up Corporal
		The Deploy trigger should be deleted
		"""	
		deploy = TriggerInstance()
		td = autoDeployTrigger(self.store)
		deploy.construct(td, self.kevin, 'Email', self.game)
		fields = [ 	( 'origin', self.corprl.serialNum() ),
					( 'destination', self.klegg.serialNum() ),
					( 'garrison', 10 ) ]
		deploy.setUserFieldsAsMap(fields)
		self.store.addObject(deploy)
		self.store.saveChanges()

		dp = DeathProbeEvent()
		dp.construct(self.game, DateTime.now(), self.scott, self.corprl)
		self.processEvents([ dp ])
		self.store.saveChanges()
		
		processor, dummy = self.makeTriggerProcessor()
		processor.processEvents(deploy, [ dp ], [])
		self.store.saveChanges()
		
		self.assertEquals(0, len(dummy.messages), dummy.messages)
		self.assertEquals(None, self.store.fetchObject(TriggerInstance, deploy.serialNum(), None))

	def testBattleMessage(self):
		"""
		Test battleMessage.py by staging a battle and then running the trigger
		"""
		
		# See testBattle.py for a longer version, and tests, of this battle sequence
		departure = DepartureEvent()
		numAttackingShips = 20
		departure.construct(self.game, DateTime.now(), self.kevin, numAttackingShips, self.corprl, self.pork, 'Ship')
		newEvents = self.processEvents([ departure ])
		arrival = newEvents[0]
		nova.BattleEvent.randomSequence = testBattle.OneThenZeros(numAttackingShips)
		try:
			newEvents = self.processEvents([ arrival ])
			battle = newEvents[0]
			newEvents = self.processEvents([ battle ])
				
			td = battleMessageTrigger(self.store)
			instance = TriggerInstance()
			instance.construct(td, self.kevin, 'Email', self.game)
			
			processor, dummy = self.makeTriggerProcessor()
			processor.processEvents(instance, [ battle ], [])
			
			self.assertEquals(1, len(dummy.messages), dummy)
			self.assertEquals(dummy.messages[0][1].subject(), 'You lost at <star name=Pork/> to scott')
			self.assertEquals(dummy.messages[0][1].body(), '<unit qty=20 /> attacked <star name=Pork/> (owner scott, <unit qty=15 />)<br/>scott won the battle, with <unit qty=14 /> remaining')
		finally:
			nova.BattleEvent.randomSequence = None
			

	def testEngineProcessing(self):
		"""
		Test engine processing of a TriggerInstance
		"""
		self.game.setTimeCompression(50000)

		# Log.enabled = 1
		
		td = battleMessageTrigger(self.store)
		instance = TriggerInstance()
		instance.construct(td, self.kevin, 'Email', self.game)
		self.store.addObject(td)
		self.store.addObject(instance)
		self.store.saveChanges()

		numAttackingShips = 20
		nova.BattleEvent.randomSequence = testBattle.OneThenZeros(numAttackingShips)
		try:
			fleet = dispatch.DispatchFleet()
			errors = fleet.execute(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), self.corprl.name(),
											  self.pork.name(), numAttackingShips)
			self.assertEquals(len(errors), 0)
			
			# Wait for the event to be processable, then run it
			time.sleep(0.75)

			dummy = DummyTransport()
			self.doSavedEvents(dummy)
			
			self.assertEquals(1, len(dummy.messages), dummy.messages)
			self.assertEquals(dummy.messages[0][1].subject(), 'You lost at <star name=Pork/> to scott')
			self.assertEquals(dummy.messages[0][1].body(), '<unit qty=20 /> attacked <star name=Pork/> (owner scott, <unit qty=15 />)<br/>scott won the battle, with <unit qty=14 /> remaining')
		finally:
			nova.BattleEvent.randomSequence = None
			# Log.enabled = 0

	def makeTriggerProcessor(self, transport=None):
		if transport is None:
			transport = DummyTransport()
		transports = { 'Email' : transport }
		return [ TriggerProcessor(transports), transport ]

if __name__=='__main__':
	#Log.enabled = 1
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
	"""
	loader = unittest.TestLoader()
	suite = loader.loadTestsFromTestCase(TestTrigger)
	testRunner = unittest.TextTestRunner()
	result = testRunner.run(suite)
	"""

