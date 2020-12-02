'''
ProductionEvent.py
'''

from GeneratedPy.GenProductionEvent import GenProductionEvent

class ProductionEvent(GenProductionEvent):
	def execute(self):
		if not self.star().isDead():
			# print 'Production Adding %d to player %s wealth' % ( self.wealth(), self.player().name() )
			self.star().addShips(self.numShips())
			self.player().addWealth(self.wealth())
