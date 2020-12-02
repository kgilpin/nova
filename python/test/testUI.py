import unittest
import sys

from nova.webui import format

class TestUI(unittest.TestCase):
	def testMessageFormat(self):
		self.assertEquals(format.formatEventMessage('<color>Spy Report: Klegg</color><br/>'),
						  '<font color="#FFFF00">Spy Report: Klegg</font><br/>')

		# Test replacing the same string twice
		self.assertEquals(format.formatEventMessage('<color><color>'),
						  '<font color="#FFFF00"><font color="#FFFF00">')

		# Test the 'ship' and 'ships' strings
		self.assertEquals(format.formatEventMessage('<unit qty=1 />'), '1 ship')
		self.assertEquals(format.formatEventMessage('<unit qty=1/>'), '1 ship')
		self.assertEquals(format.formatEventMessage('<unit qty=2 />'), '2 ships')

if __name__=='__main__':
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
