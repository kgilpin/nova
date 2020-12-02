from __future__ import nested_scopes

from nova.engine import store, find
from nova.api import method
from nova.Player import Player
from nova.Game import Game

from nova.beanContext import BeanContext
from nova.bean.snapshot import Snapshot

def getSnapshot(client, since = None, eventLimit = None):
	"""
	Return a snapshot of the current game state as beans
	See nova.beans.snapshot

	client	: may be a Player object (for internal use only), or a tuple of ( gameId, playerName, password )
	since : the time since which to return events. May be fractional. If None, no events are returned
	eventLimit : may be used to limit the absolute number of events which are returned.
		If 0, no events are returned
	"""
	client = _findClient(client)
	
	bc = BeanContext(client)
	bPlayers = [ bc.player(other) for other in find.getOtherPlayers(client) ]
	bPlayers.append(bc.player(client))
	
	bStars = [ bc.star(star) for star in find.getAllStars(client.game()) ]

	if since is not None or eventLimit > 0:
		bEvents = [ event.createBean(bc) for event in find.getPlayerEvents(client, since, limit = eventLimit) ]
	else:
		bEvents = []
	
	bFleets = [ fleet.createBean(bc) for fleet in find.getPlayerFleetsInTransit(client) ]
	
	game = client.game().createBean(bc)
	
	ss = Snapshot()
	return ss.construct(game, bStars, bPlayers, bFleets, bEvents)

def getDeploymentOrders(client, snapshot = None):
    """
	Get a map from origin (Star) to ( destination, garrison )
	Each entry represents a deployment order from the origin to the destination, leaving
	the specified garrison of ships at the origin
	
	client	: may be a Player object (for internal use only), or a tuple of ( gameId, playerName )
	snapshot : if None, a new snapshot is constructed that has no events. Otherwise the stars in that snapshot
	are used to populate the result.
    """
    
    # Get a snapshot with 0 events if there is no snapshot provided
    if snapshot is None:
	snapshot = getSnapshot(client, eventLimit = 0)
    orders = find.getDeploymentOrders(client)
    result = {}
    for star, pair in orders.items():
	destination, garrison = pair
	result[snapshot.star(star.serialNum())] = ( snapshot.star(destination.serialNum()), garrison )
    return result
    
def _findClient(client):
	if not isinstance(client, Player):
		game, playerName, password = client
		client = method.authenticatePlayer(game, playerName, password)
	return client
    