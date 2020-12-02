import method

from nova.TriggerInstance import TriggerInstance
from nova.TriggerDefinition import TriggerDefinition, battleMessageTrigger

from nova.engine import store, find

class BattleNotification(method.APIMethod):
	"""
	Enable/disable Battle notification messages for a player
	"""	
	# TODO: should lock the DB here
		
	def enable(self, gameId, playerName, password):
		game = self.game(gameId);
		player = self.login(game, playerName, password)
		
		if not find.isBattleNotificationEnabled(player):
			instance = TriggerInstance()
			instance.construct(battleMessageTrigger(store.get()), player, 'Email', player.game())
			store.get().addObject(instance)
			store.get().saveChanges()
	
	def disable(self, gameId, playerName, password):
		game = self.game(gameId);
		player = self.login(game, playerName, password)

		if find.isBattleNotificationEnabled(player):
			# Query for the TriggerInstance whose TriggerDefinition is the battleMessageTrigger
			instance = store.get().fetchObjectsOfClass(TriggerInstance, clauses="WHERE playerId = %s and triggerDefId = %s" % ( player.sqlObjRef(), battleMessageTrigger(store.get()).sqlObjRef() ))[0]
			store.get().deleteObject(instance)
			store.get().saveChanges()
	

