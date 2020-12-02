'''
Star.py
'''

import math

from nova.bean import star

from IllegalStateException import IllegalStateException
from GeneratedPy.GenStar import GenStar

def sortByName(first, second):
	return cmp(first.name().upper(), second.name().upper())

class Star(GenStar):

	def createBean(self, beanContext):
		"""
		Construct a data bean for this Star
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		ownerInfo = None
		if beanContext.client() is self.owner():
			ownerInfo = self.createStarOwnerInfo(beanContext)
		return star.Star().construct(self.serialNum(), self.name(), self.x(), self.y(), self.isDead(),
									 beanContext.player(self.owner()), ownerInfo)		

	def createStarOwnerInfo(self, beanContext):
		return star.StarOwnerInfo().construct(self.wealth(), self.numAvailableShips(), self.numFactories(),
											  self.hasSpyShield(), self.hasDeathShield())		

	def distanceTo(self, star):
		dx = self.x() - star.x()
		dy = self.y() - star.y()
		return math.sqrt(dx**2 + dy**2)

	def numAvailableShips(self):
		"""
		Returns the number of ships that are garrisoned on the star and are not scheduled to leave
		"""
		sql = "SELECT COALESCE(SUM(DE.numShips), 0) " \
			"FROM Star LEFT JOIN DepartureEvent DE ON " \
				"( ( %d << 32 | Star.starId ) = DE.originId AND DE.unitType = 'Ship' AND DE.status = 'Pending' ) " \
			"WHERE Star.starId = %d " % ( self.klass().id(), self.serialNum() )
		conn, cur = self.store().executeSQL(sql)
		assert cur.rowcount == 1
		try:
			val = cur.fetchone()
			pendingShips = val[0]
		finally:
			conn.close()
			cur.close()
		return self.numShips() - pendingShips

	def subtractShips(self, numShips):
		newNumShips = self.numShips() - numShips
		if newNumShips >= 0:
			self.setNumShips(newNumShips)
		else:
			raise IllegalStateException("Cannot remove %d ships from %s. Only %d ships are available" %
												 ( numShips, self.name(), self.numShips() ))

	def addShips(self, numShips):
		self.setNumShips(self.numShips() + numShips)


	def __str__(self):
		from nova.beanContext import BeanContext
		return str(self.createBean(BeanContext(self.owner())))
