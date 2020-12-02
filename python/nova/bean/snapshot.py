
class Snapshot:
	def construct(self, game, stars, players, fleets, events):

		# Sort the stars and players by name		
		stars.sort(lambda x, y: cmp(x.name(), y.name()))
		players.sort(lambda x, y: cmp(x.name(), y.name()))
		
		self._game = game
		self._stars = stars
		self._players = players
		self._fleets = fleets
		self._events = events
		
		for event in events:
			if event.client() is None:
				# Don't want to use str() because it may break if client() is None
				raise 'client() is None for event %s' % type(event)
		return self
		
	def game(self): return self._game
	def stars(self): return self._stars
	def players(self): return self._players
	def fleets(self): return self._fleets
	def events(self): return self._events

	def getOwnedLiveStars(self):
		client = self.clientPlayer()
		return [ star for star in self.stars() if star.owner() is client and not star.isDead() ]

	def getScores(self):
		" Get a list of ( player, score ) tuples, ordered by descending score "
		m = {}
		for player in self.players():
			m[player] = 0
		for star in self.stars():
			if star.owner() and m.has_key(star.owner()):
				m[star.owner()] += 1
		l = m.items()
		l.sort(lambda x, y: cmp(y[1], x[1]))
		return l

	def getPendingShipsByStar(self):
		"""
		Get a map from star to numShips, where numShips is the number of ships that are scheduled
		to leave the star but have not departed yet
		"""
		m = {}
		for star in self.stars():
			m[star] = 0
		for fleet in self.fleets():
			if fleet.unitType() == 'Ship' and fleet.isPending(self.game()):
				m[star] += fleet.numShips()
		return m

	def clientPlayer(self):
		" Get the player object that represents the client player "
		players = [ player for player in self.players() if player.ownerInfo() ]
		assert len(players) == 1
		return players[0]

	def player(self, name):
		for player in self.players():
			if player.name() == name:
				return player
		raise "No such player '%s' found" % name

	def star(self, nameOrId):
		for star in self.stars():
			if star.name() == nameOrId or star.id() == nameOrId:
				return star
		raise "No such star '%s' found" % nameOrId

	def __str__(self):
		stars = ""
		for star in self.stars():
			stars += "%s\n" % star
		players = ""
		for player in self.players():
			players += "%s\n" % player
		fleets = ""
		for fleet in self.fleets():
			fleets += "%s\n" % fleet
		events = ""
		for event in self.events():
			events += "%s\n" % event
		events = events[:-1]
		return "%s%s%s%s%s" % ( self.game(), players, stars, fleets, events )
