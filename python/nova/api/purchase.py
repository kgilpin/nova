import method

from nova.PurchaseFactoriesEvent import PurchaseFactoriesEvent
from nova.PurchaseRangeEvent import PurchaseRangeEvent
from nova.PurchaseSpeedEvent import PurchaseSpeedEvent
from nova.PurchaseProbeShieldEvent import PurchaseProbeShieldEvent
from nova.PurchaseDeathShieldEvent import PurchaseDeathShieldEvent

from nova.Star import Star

from mx import DateTime

class PurchaseFactories(method.APIMethod):
	def execute(self, gameId, playerName, password, starName, numFactories):
		"""
		Immediately purchase numFactories on a star
		"""
		game = self.game(gameId);
		player = self.login(game, playerName, password)
		
		star = self.findStar(game, starName)
		purchase = PurchaseFactoriesEvent()
		purchase.construct(game, DateTime.now(), player, star, numFactories)
		return self.executeEvent(purchase)

class PurchaseRange(method.APIMethod):
	def execute(self, gameId, playerName, password, range):
		"""
		Immediately purchase range for a player
		"""
		game = self.game(gameId);
		player = self.login(game, playerName, password)
		
		purchase = PurchaseRangeEvent()
		purchase.construct(game, DateTime.now(), player, range)
		return self.executeEvent(purchase)

class PurchaseSpeed(method.APIMethod):
	def execute(self, gameId, playerName, password, speed):
		"""
		Immediately purchase speed for a player
		"""
		game = self.game(gameId);
		player = self.login(game, playerName, password)
		
		purchase = PurchaseSpeedEvent()
		purchase.construct(game, DateTime.now(), player, speed)
		return self.executeEvent(purchase)

class PurchaseShield(method.APIMethod):
	def _purchase(self, gameId, playerName, password, starName, eventClass):
		game = self.game(gameId);
		player = self.login(game, playerName, password)
		star = self.findStar(game, starName)
		
		purchase = eventClass()
		purchase.construct(game, DateTime.now(), player, star)
		return self.executeEvent(purchase)

class PurchaseProbeShield(PurchaseShield):
	def execute(self, gameId, playerName, password, starName):
		"""
		Immediately purchase a spy shield on the star
		"""
		return PurchaseShield._purchase(self, gameId, playerName, password, starName, PurchaseProbeShieldEvent)

class PurchaseDeathShield(PurchaseShield):
	def execute(self, gameId, playerName, password, starName):
		"""
		Immediately purchase a death shield on the star
		"""
		return PurchaseShield._purchase(self, gameId, playerName, password, starName, PurchaseDeathShieldEvent)

