import method, cPickle

import log4py

from nova.Star import Star
from nova.TriggerInstance import TriggerInstance
from nova.TriggerDefinition import TriggerDefinition, autoDeployTrigger

from nova.api import query
from nova.engine import store

Log = None

class DeploymentOrders(method.APIMethod):
	"""
	Specify deployment orders for a star
	"""	
	def undeploy(self, gameId, playerName, password, starId):
		"""
		Remove the deployment orders for a player's star, identified by its ID
		"""
		game = self.game(gameId)
		player = self.login(game, playerName, password)
		
		Log.debug('Undeploying from origin star %s' % self.starName(starId))
		
		# Find all the Deployment TriggerInstances for the player
		# Remove the one which refers to the specified star
		instances = store.get().fetchObjectsOfClass(TriggerInstance, clauses="WHERE playerId = %s and triggerDefId = %s" % ( player.sqlObjRef(), autoDeployTrigger(store.get()).sqlObjRef() ))
		removed = 0
		for instance in instances:
			fields = instance.getUserFieldsMap()
			originId = store.get().fetchObject(Star, fields['origin']).serialNum()
			if originId == starId:
				store.get().deleteObject(instance)
				store.get().saveChanges()
				removed = 1
		if not removed:
			message = "No deployment orders found for star '%s'" % self.starName(starId)
			return { starId : message }
	
	def deploy(self, gameId, playerName, password, originId, destinationId, garrison):
		"""
		Create deployment orders from originId to destinationId
		"""			
		game = self.game(gameId)
		player = self.login(game, playerName, password)

		Log.debug('Deploying from %s to %s with garrison %d' % ( self.starName(originId), self.starName(destinationId), garrison ))
		
		self.undeploy(gameId, playerName, password, originId)
		
		# Make sure originId and destinationId are valid
		self.starName(originId)
		self.starName(destinationId)
		
		instance = TriggerInstance()
		instance.construct(autoDeployTrigger(store.get()), player, 'Email', player.game())
		fields = [ 	( 'origin', originId ),
					( 'destination', destinationId ),
					( 'garrison', garrison ) ]
		instance.setUserFieldsAsMap(fields)
		
		store.get().addObject(instance)
		store.get().saveChanges()
		
Log = log4py.Logger().get_instance(DeploymentOrders)
	