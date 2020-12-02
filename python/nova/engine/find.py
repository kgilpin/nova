from __future__ import nested_scopes

from nova.engine import store
from nova.ArrivalEvent import ArrivalEvent
from nova.BattleEvent import BattleEvent
from nova.DeathProbeEvent import DeathProbeEvent
from nova.DepartureEvent import DepartureEvent
from nova.FieryDeathEvent import FieryDeathEvent
from nova.Game import Game
from nova.GlobalProductionEvent import GlobalProductionEvent
from nova.TriggerDefinition import battleMessageTrigger, autoDeployTrigger
from nova.TriggerInstance import TriggerInstance
from nova.Player import Player
from nova.SpyProbeEvent import SpyProbeEvent
from nova.Star import Star
from nova.Event import Event

def isBattleNotificationEnabled(player):
	"""
	Return true if battle notification e-mail is enabled for the player
	"""
	# Query for the TriggerInstance whose TriggerDefinition is the battleMessageTrigger
	instances = store.get().fetchObjectsOfClass(TriggerInstance, clauses="WHERE playerId = %s and triggerDefId = %s" % ( player.sqlObjRef(), battleMessageTrigger(store.get()).sqlObjRef() ))
	return len(instances) > 0

def getDeploymentOrders(player):
	"""
	Get a map from origin (Star) to ( destination, garrison )
	Each entry represents a deployment order from the origin to the destination, leaving
	the specified garrison of ships at the origin
	"""
	instances = store.get().fetchObjectsOfClass(TriggerInstance, clauses="WHERE playerId = %s and triggerDefId = %s" % ( player.sqlObjRef(), autoDeployTrigger(store.get()).sqlObjRef() ))
	result = { }
	for instance in instances:
		fields = instance.getUserFieldsMap()
		origin = store.get().fetchObject(Star, fields['origin'])
		destination = store.get().fetchObject(Star, fields['destination'])
		garrison = fields['garrison']
		result[origin] = ( destination, garrison )
	return result		

def getAllStars(game):
	"""
	Get all the stars in the game, sorted by star name
	"""
	return store.get().fetchObjectsOfClass(Star, clauses="WHERE gameId = %s ORDER BY name ASC" % game.sqlObjRef())

def getOwnedLiveStars(player):
	"""
	Get all stars owned by the player which are not dead.
	"""
	return store.get().fetchObjectsOfClass(Star, clauses="WHERE ownerId = %s AND isDead = 0 ORDER BY name ASC"% player.sqlObjRef())

def getOtherPlayers(player):
	"""
	Get all the other Player objects besides this one
	"""
	return store.get().fetchObjectsOfClass(Player, clauses="WHERE gameId = %s AND name != '%s' AND name != 'Nobody' ORDER BY name ASC" \
		% ( player.game().sqlObjRef(), player.name() ))

def getPlayerFleetsInTransit(player):
	"""
	Get all fleets which are in transit. This is all fleets whose arrival time is after the last time the game actions
	were processed, plus all fleets whose status is 'Pending'
	"""
	fleets = []
	fleets.extend( store.get().fetchObjectsOfClass(DepartureEvent, clauses="WHERE playerId = %s AND status='Pending' ORDER BY arrivalTime ASC" % \
			( player.sqlObjRef() ) ) )
	if player.game().lastActionTime() is not None:
		fleets.extend( store.get().fetchObjectsOfClass(DepartureEvent, clauses="WHERE playerId = %s AND status='Complete' AND arrivalTime > '%s' ORDER BY arrivalTime ASC" % \
			( player.sqlObjRef(), formatMySQLDate(player.game().lastActionTime()) ) ) )
	return fleets

def getPendingShipsByStar(game):
	"""
	Return a map from starId to numShips, where numShips is the number of ships that are scheduled
	to leave the star but have not departed yet
	"""
	sql = "SELECT starId, COALESCE(SUM(DE.numShips), 0) " \
		"FROM Star LEFT JOIN DepartureEvent DE ON " \
			"( ( %d << 32 | Star.starId ) = DE.originId AND DE.unitType = 'Ship' AND DE.status = 'Pending' ) " \
		"WHERE Star.gameId = %d " \
		"GROUP BY starId" % ( Star().klass().id(), game.sqlObjRef() )
	conn, cur = store.get().executeSQL(sql)
	pendingShips = {}
	try:
		for row in cur.fetchall():
			pendingShips[row[0]] = int(row[1])
	finally:
		conn.close()
		cur.close()
	return pendingShips

def getPlayerScores(game):
	"""
	Get the name and current score for each player in the game. 
	Returns a list of tuples ( name, score )
	"""
	nobody = game.nobody()
	klassId = nobody.klass().id()
	# Here we are reconstructing the MiddleKit 'sqlObjRef' function which is used to create
	#   foreign keys. See MiddleKit.Core.ObjRefAttr.objRefJoin
	conn, cur = store.get().executeSQL("SELECT Player.name, COUNT(*) FROM Player, Star " \
		"WHERE Star.gameId = %s AND Star.ownerId = ( %d << 32 | Player.playerId ) AND Player.name <> 'Nobody' " \
		"GROUP BY Player.name " % ( game.sqlObjRef(), klassId ) )
	scores = []
	try:
		for row in cur.fetchall():
			scores.append( ( row[0], row[1] ) )
	finally:
		conn.close()
		cur.close()
		
	# Find all the Players with score = 0
	conn, cur = store.get().executeSQL("SELECT Player.name " \
			"FROM Player LEFT JOIN Star ON Star.ownerId = ( %d << 32 | Player.playerId ) " \
           	"WHERE Player.gameId = %s AND Star.starId IS NULL AND Player.name <> 'Nobody'"  % ( klassId, game.sqlObjRef() ) )
	try:
		for row in cur.fetchall():
			scores.append( ( row[0], 0 ) )
	finally:
		conn.close()
		cur.close()

		
	# Sort by score, for some reason I can't do ORBER BY in the query
	scores.sort(lambda first, second: int(second[1] - first[1]))
	return scores

def nextProductionTime(game):
	"""
	Return the time of the next GlobalProductionEvent, or None if there are no more production
	events scheduled before the end of the game.
	"""
	gps = store.get().fetchObjectsOfClass(GlobalProductionEvent, 
		clauses="WHERE gameId = %s AND status='Pending' ORDER BY executionTime DESC LIMIT 1" % game.sqlObjRef())
	if len(gps)	!= 0:
		return gps[0].executionTime()
	else:
		return None
		
def getPlayerEvents(player, since, limit=None, filterFunc=None):
	"""
	Get all the Events which are owned by the Player and have occured since the time 'since'
	  They are ordered from newest to oldest
	The number of events returned can be limited by the 'limit' argument
	'filterFunc' may be a function which is used to filter the results of the query
	"""

	def _eventQuery(cls, filterPlayer = None, filterClauses=[]):
		"""
		Queries for events of class 'cls', using the clause:
		[ WHERE playerId = <player> ] [ AND? <filterClause> ] ORDER BY executionTime DESC
		"""
		game = player.game()
		whereClauses = []
		if filterPlayer is not None:
			whereClauses.append("playerId = %s" % filterPlayer.sqlObjRef())
		else:
			whereClauses.append("gameId = %s" % game.sqlObjRef())
			whereClauses.extend(filterClauses)
			
		clause = "WHERE status = 'Complete' AND executionTime >= '%s'" % formatMySQLDate(since)
		if len(whereClauses):
			clause += " AND " + " AND ".join(whereClauses)
			clause += " ORDER BY executionTime DESC"
		if limit is not None:
			clause += " LIMIT %d" % limit
		return store.get().fetchObjectsOfClass(cls, clauses=clause)		

	ownedStars = getOwnedLiveStars(player)
	ownedStarIds = ', '.join([ str(star.sqlObjRef()) for star in ownedStars ])
	
	# Events which are shown in the UI are:
	#   GlobalProductionEvent (all)
	#   ArrivalEvent (self)
	#   SpyProbeEvent (self)
	#   DeathProbeEvent (self, or hasDeathShield = false)
	#   FieryDeathEvent (self)
	#   BattleEvent WHERE victor = attacker (all)
	#   BattleEvent WHERE attacker = self (all)
	#   BattleEvent WHERE defender = self (all)
	events = []
	events.extend(_eventQuery(GlobalProductionEvent))
	events.extend(_eventQuery(ArrivalEvent, filterPlayer=player))
	events.extend(_eventQuery(SpyProbeEvent, filterPlayer=player))
	if len(ownedStars):
		events.extend(_eventQuery(SpyProbeEvent, filterClauses=[ "hasSpyShield = 1 AND starId IN ( %s ) " % ownedStarIds ]))
	events.extend(_eventQuery(DeathProbeEvent, filterPlayer=player))
	events.extend(_eventQuery(DeathProbeEvent, filterClauses=[ "hasDeathShield = 0 AND playerId <> %d" % player.sqlObjRef() ]))
	if len(ownedStars):
		events.extend(_eventQuery(DeathProbeEvent, filterClauses=[ "hasDeathShield = 1 AND starId IN ( %s ) " % ownedStarIds ]))
	events.extend(_eventQuery(FieryDeathEvent, filterPlayer=player))

	battleEvents = []
	battleEvents.extend(_eventQuery(BattleEvent, filterClauses=[ "victorId = attackerId" ]))
	battleEvents.extend(_eventQuery(BattleEvent, filterClauses=[ "attackerId = %s" % player.sqlObjRef() ]))
	battleEvents.extend(_eventQuery(BattleEvent, filterClauses=[ "defenderId = %s" % player.sqlObjRef() ]))
	# Filter duplicates out of the BattleEvents
	battleEventMap = {}
	for event in battleEvents:
		if not battleEventMap.has_key(event):
			battleEventMap[event] = event
			events.append(event)

	if filterFunc is not None:
		events = filter(filterFunc, events)

	events.sort(lambda first, second: int( ( second.executionTime() - first.executionTime() ).seconds ) )

	if limit is not None:
		events = events[:limit]
		
	return events		
	
def formatMySQLDate(date):
	return date.Format('%Y-%m-%d %H:%M:%S')

