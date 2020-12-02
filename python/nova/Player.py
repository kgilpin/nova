'''
Player.py
'''


from nova.bean import player
from GeneratedPy.GenPlayer import GenPlayer


class Player(GenPlayer):
	def createBean(self, beanContext):
		"""
		Construct a data bean for this Player
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		ownerInfo = None
		if beanContext.client() is self:
			ownerInfo = player.PlayerOwnerInfo().construct(self.adjustedSpeed(), self.range(), self.wealth(), self.availableCash())
		return player.Player().construct(self.name(), ownerInfo)
	
	def adjustedSpeed(self):
		"""
		Return the player's movement speed, adjusted for the game timeCompression factor
		"""
		return self.speed() * self.game().timeCompression()

	def availableCash(self):
		"""
		Returns the amount of cash that is not scheduled to be spent
		"""
		cost = self._pendingCost(self.game().spyProbeCost(), 'SpyProbe')
		cost += self._pendingCost(self.game().deathProbeCost(), 'DeathProbe')
		return self.wealth() - cost
	
	def addWealth(self, delta):
		self.setWealth(self.wealth() + delta)

	def subtractWealth(self, delta):
		self.setWealth(self.wealth() - delta)

	def _pendingCost(self, cost, unitType):		
		sql = "SELECT COUNT(*) " \
			"FROM DepartureEvent DE " \
			"WHERE DE.playerId = %s AND DE.unitType = '%s' AND DE.status = 'Pending'" % \
				( self.sqlObjRef(), unitType )
		conn, cur = self.store().executeSQL(sql)
		assert cur.rowcount == 1
		try:
			val = cur.fetchone()
			return val[0] * cost
		finally:
			conn.close()
			cur.close()
		
	def __str__(self):
		from nova.beanContext import BeanContext
		return str(self.createBean(BeanContext(self)))
		
