import random

import log4py
import starNames

from nova.Game import Game
from nova.GlobalProductionEvent import GlobalProductionEvent, nextProductionTime
from nova.Star import Star
from nova.Player import Player
from nova.User import User

from mapLoader import StarMap

from mx import DateTime

class GameConstructionException(Exception):
	pass

Log = None

NUM_ITERATIONS = 250
AVERAGE_WEALTH = 5
AVERAGE_NUMSHIPS = 10
HOME_WEALTH = 10
HOME_NUMSHIPS = 250
PLAYER_RANGE = 15

class StarNamer:
	"""
	This class names all the stars
	"""
	def __init__(self):
		self._stars = starNames.StarParser().stars()
		self._index = 0
	
	def nextName(self):
		if len(self._stars) == 0:
			self._index += 1
			return "star%d" % self._index
		else:
			index = random.random() * len(self._stars)
			star = self._stars.pop(index)
			# Star names may be constructed as Unicode by the XML parser, this convertss them to regular strings
			return str(star[0])

class StarPopulator:
	"""
	This class assigns the wealth values to all the stars in a map, and also assigns
	home worlds to players
	"""
	def __init__(self, stars, homeWorlds, players):
		"""
		stars : list of all stars in the map
		homeWorlds : list of stars which are homeworlds
		players : list of all players (except Nobody)
		"""
		i = 0
		homeWorldByIndex = {}
		for star in homeWorlds:
			homeWorldByIndex[i] = star
			i += 1

		"""
		Try a large number of different assignments of players to home worlds
		Evaluate a balanced-ness metric for each one and pick the one which is most balanced
		Here the metric is the number of stars that are closer to that home world than to any other
		The goal is to maximumize the minimum value of the metric
		"""

		startTime = DateTime.now()
		
		bestHomes = None
		bestAdjacentStars = None
		maxMetric = 0
		for i in range(NUM_ITERATIONS):
			homeWorldsCopy = homeWorlds[:]
			selectedHomes = []
			adjacentStars = {}

			for player in players:
				if not len(homeWorldsCopy):
					raise GameConstructionException("Not enough home worlds ( %d ) in the map for all the players ( % d)" %
													( len(homeWorlds), len(players) ))
				
				index = int( random.random() * len(homeWorldsCopy) )
				homeWorld = homeWorldsCopy.pop(index)
				selectedHomes.append(homeWorld)
				adjacentStars[homeWorld] = []

			# Assign each star to the closest home star
			#   Save the list of adjacent stars for each home star
			for star in stars:
				if not star in selectedHomes:
					minDistance = 10 ** 6
					owner = None
					for home in selectedHomes:
						distance = home.distanceTo(star)
						if distance < minDistance or \
							   distance == minDistance and random.random() < 0.5:
							minDistance = distance
							owner = home
					# print 'owner of %s is %s' % ( star.name(), home.name() )
					adjacentStars[owner].append( star )

			# Find the smallest count of adjacentStars across all the selected home worlds
			metric = reduce(lambda first, second: min(first, len(second)), adjacentStars.values(), 10 ** 6)
			if metric > maxMetric:
				maxMetric = metric
				Log.info('Stars per player : %d' % maxMetric)
				bestHomes = selectedHomes
				bestAdjacentStars = adjacentStars

		endTime = DateTime.now()
		Log.info('Ran %d iterations of home world selection algorithm in %s' % ( NUM_ITERATIONS, endTime - startTime ))
		
		remainingPlayers = players[:]

		assert len(bestHomes) == len(remainingPlayers), 'Number of homeWorlds and number of players is different'
		
		for star in stars:
			if star not in bestHomes:
				star.setNumShips(int( random.random() * AVERAGE_NUMSHIPS * 2 ))

		for star in bestHomes:
			index = int( random.random() * len(remainingPlayers) )
			owner = remainingPlayers.pop(index)
			star.setOwner(owner)
			Log.debug('(%d,%d) is the home world for %s' % ( star.x(), star.y(), owner.name() ))
			# print '%s.name = %s' % ( star.name(), owner.name() )
			star.setName(owner.name())
			star.setWealth(HOME_WEALTH)
			star.setNumShips(HOME_NUMSHIPS)

		for starList in bestAdjacentStars.values():
			# Total wealth assigned to each player is the star-metric * AVERAGE_WEALTH
			# Assign the wealth randomly to its adjacent stars
			playerWealth = maxMetric * AVERAGE_WEALTH
			while playerWealth > 0:
				index = int( random.random() * len(starList) )
				star = starList[index]
				star.setWealth(star.wealth() + 1)
				playerWealth -= 1
			
class NewGame:
	def __init__(self, starMap, users, startTime, duration, store, timeCompression=1):
		"""
		Construct a new game from a StarMap, a list of player names, a
		startTime, and a duration
		"""

		endTime = startTime + duration

		game = Game()
		game.construct(startTime, endTime)
		game.setTimeCompression(timeCompression)
		store.addObject(game)
		store.saveChanges()

		# Find or add the 'Nobody' user
		nobodies = store.fetchObjectsOfClass(User, clauses="WHERE name = 'Nobody'")
		if len(nobodies):
			nobody = nobodies[0]
		else:
			nobody = User()
			nobody.construct('Nobody', 'nobody', '')
			store.addObject(nobody)

		users.append(nobody)
		
		players = []
		for user in users:
			player = Player()
			player.construct(game, user, user.name())
			player.setRange(PLAYER_RANGE)
			players.append(player)
			store.addObject(player)

		# Hide the 'nobody' user, store the 'nobody' player
		nobodyPlayer = players.pop()
		users.pop()
		del nobody

		namer = StarNamer()

		homeWorlds = []
		stars = []
		for starData in starMap.starData():
			star = Star()
			star.construct(game, namer.nextName(), starData[0], starData[1])
			store.addObject(star)
			stars.append(star)
			if starMap.isHomeWorld(starData):
				homeWorlds.append(star)

		# Assign the players to home worlds and populate the star wealth
		StarPopulator(stars, homeWorlds, players)

		for star in stars:
			if star.owner() is None:
				star.setOwner(nobodyPlayer)

		store.saveChanges()
				
		# Finally, create a new GlobalProductionEvent
		gp = GlobalProductionEvent()
		gp.construct(game, nextProductionTime(game.startTime(), game))
		store.addObject(gp)
		
		store.saveChanges()

		self._game = game
		self._players = players
		self._stars = stars

	def game(self):
		return self._game

	def players(self):
		return self._players

	def stars(self):
		return self._stars

Log = log4py.Logger().get_instance(NewGame)
