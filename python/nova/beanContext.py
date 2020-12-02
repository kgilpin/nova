from mx import DateTime

class BeanContext:
	"""
	Used to store a mapping from bean identifiers to beans as they are constructed for the
	external API. See the createBean methods on the various externally visible objects.
	"""
	def __init__(self, client):
		self._client = client
		self._starsById = {}
		self._playersByName = {}
		self._now = DateTime.now()

	def client(self):
		"""
		Player which is requesting the beans
		"""
		return self._client

	def currentTime(self):
		return self._now

	def addEvent(self, event):
		event._client = self.player(self._client)
		return event

	def player(self, player):
		""" Find or create a Player bean """
		if player is None:
			return None
		if not self._playersByName.has_key(player.name()):
			bPlayer = player.createBean(self)
			self._playersByName[player.name()] = bPlayer
		return self._playersByName[player.name()]

	def star(self, star):
		""" Find or create a Star bean """
		if star is None:
			return None
		if not self._starsById.has_key(star.serialNum()):
			bStar = star.createBean(self)
			self._starsById[star.serialNum()] = bStar
		return self._starsById[star.serialNum()]

