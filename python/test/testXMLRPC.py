import unittest
import sys
import xmlrpclib
from mx import DateTime

from nova.client import api
from nova.xmlrpc.Marshal import Marshal
from nova.Star import Star
from nova.Player import Player
from nova.DepartureEvent import DepartureEvent

from basicGalaxy import BasicGalaxy

class TestXMLRPC(BasicGalaxy):
	"""
	Test using the XML-RPC API
	The server should be set up and running on localhost, with the servlet available at /cgi-bin/OneShot.cgi/Nova/XMLRPCAPI.py
	"""

	def setUp(self):
		BasicGalaxy.setUp(self)
		self.server = xmlrpclib.Server('%s/XMLRPCAPI.py' % self.novaURL())
		self.nova = api.API(self.novaURL(), self.game.serialNum(), self.kevin.name(), self.kevin.user().password())

	def testSnapshot(self):
		""" Retrieve a Snapshot directly through the xmlrpclib API and verify its contents """
		resultMap = self.server.getSnapshot(self.game.serialNum(), self.kevin.name(), self.kevin.user().password(), 1)
		self.assertEquals(1, resultMap['succeeded'], resultMap)
		ss = Marshal().unmarshal(resultMap['result'])

		self.verifySnapshot(ss)

	def testClientAPISnapshot(self):
		""" Obtain the game snapshot through the nova.client.api module """
		ss = self.nova.getSnapshot(1)
		self.verifySnapshot(ss)
		
	def verifySnapshot(self, ss):
		""" Verify the contents of a Snapshot on the basicGalaxy starting game configuration """
		self.assertEquals(2, len(ss.players()))
		self.assertEquals(3, len(ss.stars()))
		
		kevin = ss.players()[0]
		self.assertEquals('kevin', kevin.name())
		self.assertNotEquals(None, kevin.ownerInfo())
		self.assertEquals(kevin, kevin.ownerInfo().player())
		self.assertEquals(10, kevin.ownerInfo().range())
		
		scott = ss.players()[1]
		self.assertEquals('scott', scott.name())
		self.assertEquals(None, scott.ownerInfo())
		
		corprl = ss.stars()[0]
		self.assertEquals('Corporal', corprl.name())
		self.assertEquals(10, corprl.x())
		self.assertEquals(15, corprl.y())
		self.assertNotEquals(None, corprl.ownerInfo())
		self.assertEquals(200, corprl.ownerInfo().numShips())
		self.assertEquals(0, corprl.ownerInfo().hasProbeShield())

		klegg = ss.stars()[1]
		self.assertEquals('Klegg', klegg.name())
		self.assertNotEquals(None, klegg.ownerInfo())

		pork = ss.stars()[2]
		self.assertEquals('Pork', pork.name())
		self.assertEquals(None, pork.ownerInfo())
	
	def testBadPassword(self):
		# Send 20 ships from Corprl to Klegg
		nova = api.API(self.novaURL(), self.game.serialNum(), self.kevin.name(), "badpassword")
		self.failUnlessRaises(api.APIException, nova.getSnapshot, 0)

	def testFleet(self):
		# Send 20 ships from Corprl to Klegg
		ss = self.nova.getSnapshot(0)
		self.nova.dispatchFleet(ss.star('Corporal'), ss.star('Klegg'), 20)

		# Re-load the star from the database because it has changed underneath us
		self.corprl = self.store.fetchObjectsOfClass(Star, serialNum=self.corprl.serialNum(), refreshAttrs=1)[0]
		self.assertEquals(self.corprl.numShips(), 180)

	def testProbe(self):
		# Send a probe from Corprl to Pork
		ss = self.nova.getSnapshot(0)
		self.nova.dispatchProbe(ss.star('Corporal'), ss.star('Pork'))

		# Re-load 'kevin' from the database because it has changed underneath us
		self.kevin = self.store.fetchObjectsOfClass(Player, serialNum=self.kevin.serialNum(), refreshAttrs=1)[0]
		self.assertEquals(self.kevin.wealth(), 250 - self.game.spyProbeCost())

	def testNovaBomb(self):
		# Send a nova bomb from Corprl to Pork
		ss = self.nova.getSnapshot(0)
		self.nova.dispatchNovaBomb(ss.star('Corporal'), ss.star('Pork'))

		# Re-load 'kevin' from the database because it has changed underneath us
		self.kevin = self.store.fetchObjectsOfClass(Player, serialNum=self.kevin.serialNum(), refreshAttrs=1)[0]
		self.assertEquals(self.kevin.wealth(), 250 - self.game.deathProbeCost())

	def testFleetWithDelay(self):
		# Send 20 ships from Corprl to Klegg, leaving in 10 minutes
		startTime = DateTime.now()
		# The executionTime of the constructed event should be after this
		expectedEndTime = DateTime.now() + DateTime.DateTimeDelta(0, 0, 9)

		ss = self.nova.getSnapshot(0)
		self.nova.dispatchFleet(ss.star('Corporal'), ss.star('Klegg'), 20, 10)

		# Re-load the star from the database because it has changed underneath us
		self.corprl = self.store.fetchObjectsOfClass(Star, serialNum=self.corprl.serialNum(), refreshAttrs=1)[0]
		event = self.store.fetchObjectsOfClass(DepartureEvent, clauses="WHERE gameId = %d" % self.game.sqlObjRef())[0]
		self.assertEquals(self.corprl.numShips(), 200)
		
		self.failUnless(event.executionTime() >= expectedEndTime)
		
if __name__=='__main__':
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
