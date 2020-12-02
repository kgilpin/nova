import unittest, time
import sys
from mx import DateTime
import log4py

from nova.DepartureEvent import travelTime

from nova.engine.Engine import Engine
from nova.util import Log

import abstractSystemTest

class SystemDeployment(abstractSystemTest.AbstractSystemTest):
	"""
	System test for automated fleet deployment (automatically sending ships from one
	star to another)
	"""
	
	def testDeployment(self):
		# First dispatch 50 ships from Kevin to Beid
		kevin = self.star("Kevin")
		beid = self.star("Beid")
		alderamin = self.star("Alderamin")
		bogardus = self.star("Bogardus")

		# First dispatch 50 ships from Kevin to Beid
		self.dispatch("kevin", kevin, beid, 50)

		# Now dispatch another 200 ships from Kevin to Alderamin
		# These should be routed through Beid
		self.dispatch("kevin", kevin, alderamin, 200)
		self.wait(travelTime(beid, alderamin, self.player('kevin'), 'Ship'))
		self.engineTick()		
		self.assertEquals(alderamin.owner(), self.player("kevin"))
		
		# Route ships from Alderamin to Kevin
		# Leave a garrison of 5 ships
		self.deploy("kevin", alderamin, kevin, 5)
	
		# Send 1 ship from Beid to Alderamin
		# They should arrive at Alderamin and then get routed to Kevin
		self.dispatch("kevin", beid, alderamin, 1)
		self.wait(travelTime(beid, alderamin, self.player('kevin'), 'Ship'))
		self.engineTick()		
		
		self.assertEquals(alderamin.numShips(), 5)
	

if __name__=='__main__':
	#Log.enabled = 1
	#log4py.Logger().get_root().set_loglevel(log4py.LOGLEVEL_DEBUG)
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
