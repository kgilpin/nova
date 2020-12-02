'''
GlobalProductionEvent.py
'''


from Player import Player
from Star import Star
from ProductionEvent import ProductionEvent
from GeneratedPy.GenGlobalProductionEvent import GenGlobalProductionEvent
from nova.bean import event

from mx import DateTime

def nextProductionTime(thisTime, game):
	"""
	Computes the next time that a GlobalProductionEvent should be scheduled, based on
	the specified time
	"""
	# Construct a delta of 1 day, and divide by game.timeCompression
	delta = DateTime.DateTimeDelta(1)
	return thisTime + delta / game.timeCompression()

def formatMySQLDate(date):
	return date.Format('%Y-%m-%d %H:%M:%S')

class GlobalProductionEvent(GenGlobalProductionEvent):
	"""
	Implements the game-wide production event. A ProductionEvent instance is created for every
	star that is not dead and is owned by a player in the game.	
	"""

	def createBean(self, beanContext):
		"""
		Construct a ProductionEvent bean
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		return beanContext.addEvent( event.ProductionEvent().construct(self.executionTime(), *self.computeNumShipsAndCash(beanContext.client())) )

	def computeNumShipsAndCash(self, client):
		# TODO: this query is really a pretty crude heuristic, finding all ProductionEvents which occurred
		#   after, but not more than 1 minute after, the GlobalProductionEvent
		sql = "SELECT COALESCE(SUM(numShips), 0), COALESCE(SUM(wealth), 0) " \
			"FROM ProductionEvent " \
			"WHERE globalProductionEventId = %s AND playerId = %s" % ( self.sqlObjRef(), client.sqlObjRef() )
		conn, cur = self.store().executeSQL(sql)
		assert cur.rowcount == 1
		try:
			val = cur.fetchone()
			numShips, cash = val
		finally:
			conn.close()
			cur.close()
		
		if numShips is None: numShips = 0
		if cash is None: cash = 0
		return numShips, cash

	def construct(self, game, executionTime):
		"""
		Constructs a new GlobalProductionEvent. The mandatory 'player' is set to the player 'Nobody' who should
		always be in the game. This is really just a placeholder since each Event requires a Player
		"""
		nobody = game.nobody()
		GenGlobalProductionEvent.construct(self, game, executionTime, nobody)

	def execute(self):
		time = DateTime.now()
		events = []
		nobody = self.game().nobody()
		players = self._mk_store.fetchObjectsOfClass(Player, clauses="WHERE gameId = %d" % self.game().sqlObjRef())
		for player in players:
			if player is not nobody:
				stars = self._mk_store.fetchObjectsOfClass(Star, clauses="WHERE ownerId = %d" % player.sqlObjRef())
				for star in stars:
					if not star.isDead():
						if star.numFactories() > 0 or star.wealth() > 0:
							event = ProductionEvent()
							event.construct(self.game(), time, player, star, star.numFactories(), star.wealth(), self)
							events.append(event)

		# Create a new GlobalProductionEvent at the appropriate time in the future
		# ( once per day, adjusted by game.timeCompression )
		newTime = nextProductionTime(self.executionTime(), self.game())
		if newTime < self.game().endTime():
			gp = GlobalProductionEvent()
			gp.construct(self.game(), newTime)
			events.append(gp)
		
		return events

	
