import unittest
import sys
import log4py

from MiddleKit.Run.MySQLObjectStore import MySQLObjectStore

from nova.engine import find
from nova.User import User
from nova.Player import Player
from nova.engine import mapLoader, newGame, starNames
    
import novaTest
import connection

from mx import DateTime

class TestNewGame(novaTest.NovaTest):
	def setUp(self):
		self.store = connection.get()
	
	def testNewGame(self):
		"""
		Test creating a new game by creating Users, loading a Map, and populating the Stars
		"""
		
		"""
		Need to set the 'ondelete' options before this will work
		
		# Clean up the old Users created by this test if they are hanging around
		whereClause = "WHERE name IN ( 'newgame-kevin', 'newgame-scott' )"
		users = self.store.fetchObjectsOfClass(User, clauses=whereClause)
		for user in users:
			self.store.deleteObject(user)
		self.store.saveChanges()
		"""
		
		loader = mapLoader.ImageMapLoader('../maps/scatter.bmp')
		map = loader.loadStarMap()

		kUser = self.makeUser('newgame-kevin', 'kevin', 'k@kevin.com')
		sUser = self.makeUser('newgame-scott', 'scott', 's@scott.com')

		self.store.addObject(kUser)
		self.store.addObject(sUser)

		self.store.saveChanges()

		startTime = DateTime.now()
		# Make a game that lasts for 1 hour
		duration = DateTime.DateTimeDelta(0, 1)

		new = newGame.NewGame(map, [ kUser, sUser ], startTime, duration, self.store)

		print 'New game : %d' % new.game().serialNum()

		self.assertEquals(new.game().endTime() - new.game().startTime(), duration)
		self.assertEquals(len(new.players()), 2)
		self.assertEquals(new.players()[0].game(), new.game())

		nobody = self.store.fetchObjectsOfClass(Player, clauses="WHERE gameId = %s and name = 'Nobody'" % new.game().sqlObjRef())[0]

		self.assertEquals(len([star for star in new.stars() if star.owner() is None]), 0)

		homeWorlds = [star for star in new.stars() if star.owner() is not nobody]

		self.assertEquals(len(homeWorlds), 2)
		
		nextProduction = find.nextProductionTime(new.game())
		self.assertNotEquals(nextProduction, None)

	def testStarNames(self):
		parser = starNames.StarParser()
		stars = parser.stars()

		# Find the first star, the last one, and one in the middle
		self.failUnless((u'Acamar', u'3.24') in stars)	
		self.failUnless((u'Polaris', u'2.02') in stars)	
		self.failUnless((u'Q Car', u'3.36') in stars)	

		# Make sure there are no duplicates
		nameMap = {}
		duplicates = []
		for name, mag in stars:
			if nameMap.has_key(name):
				duplicates.append(name)
			nameMap[name] = name

		self.assertEquals([], duplicates)

if __name__=='__main__':
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
