from NovaPage import NovaPage

from nova.Game import Game
from nova.Player import Player

class GamePage(NovaPage):
	def game(self):
		return self._game

	def player(self):
		return self._player

	def login(self, returnToURL="console.psp"):
		"""
		Return true if the user is logged in. This is determined by looking at browser cookies.
		"""
		if not NovaPage.login(self, returnToURL):
			return 0;
		
		if not self.request().hasValue('gameId') or \
			not self.request().hasValue('playerId'):
			self.response().sendRedirect('/nova/selectMatch.psp?returnToURL=%s' % returnToURL)
			return 0

		self._game = self.store().fetchObject(Game, int(self.request().value('gameId')))
		self._player = self.store().fetchObject(Player, int(self.request().value('playerId')))
		
		return 1

	def _credentials(self):
		"""
		Returns a list of [ game.serialNum(), playerName, password ]
		"""
		return [ self._game.serialNum(), self._player.name(), self.request().value('password') ]
	

