import sys, unittest
import basicGalaxy

from nova.api import comm

# This file is not named 'testMail' because we don't want it to run all the time
# Getting e-mail every time we run the test suite would be annoying

class TestMail(basicGalaxy.BasicGalaxy):
	def testPlayerToPlayer(self):
		"""
		Tests sending e-mail from one player to another
		"""
		mail = comm.PlayerToPlayerMail()
		result = mail.send(self.game.serialNum(), "scott", "scott", "kevin", 
			'testMail', 'this is a message sent from testMail.py')
		self.assertEquals(len(result), 0)
		
if __name__=='__main__':
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
			