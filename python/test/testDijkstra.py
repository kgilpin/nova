import unittest, sys, math

from nova.trigger import dijkstra
from nova.DepartureEvent import buildStarGraph

class Star:
	"""
	Simple 2-d star
	"""
	def __init__(self, name, x, y):
		self._name = name
		self._x = x
		self._y = y
	
	def distanceTo(self, other):
		dx = self._x - other._x
		dy = self._y - other._y
		return math.sqrt(dx * dx + dy * dy)

	def __repr__(self):
		return "%s (%d,%d)" % ( self._name, self._x, self._y )

	
"""
 012345
0a  b
1     c
2d e
3    
4f    g
"""

a = Star('alpha', 0, 0)
b = Star('bingo', 0, 3)
c = Star('charlie', 1, 5)
d = Star('dingo', 2, 0)
e = Star('echo', 2, 2)
f = Star('foxhole', 4, 0)
g = Star('gamma', 4, 5)

stars = [ a, b, c, d, e, f, g]

class TestDijkstra(unittest.TestCase):
	"""
	Tests operation of the Dijkstra shortest path algorithm used for star routing
	"""
	
	def testG(self):
		"""
		Tests computing the edge graph G
		"""
		range = 2
		graph = buildStarGraph(stars, range)

		# Test that the count of the reachable stars is correct		
		self.assertEquals(1, len(graph[a]))
		self.assertEquals(3, len(graph[d]))
		self.assertEquals(0, len(graph[g]))
							  
		self.assertEquals(2, graph[a][d])					  

	def testShortestPath(self):
		"""
		Tests computing the stortest path between stars
		"""
		range = 2
		graph = buildStarGraph(stars, range)
		
		# From a to f (a, d, f)
		path = dijkstra.shortestPath(graph, a, f)
		self.assertEquals(path, [ a, d, f ])

		path = dijkstra.shortestPath(graph, f, a)
		self.assertEquals(path, [ f, d, a ])
		
		# From d to e (d, e)
		path = dijkstra.shortestPath(graph, d, e)
		self.assertEquals(path, [ d, e ])
		
		# From e to g (no path)
		self.failUnlessRaises(KeyError, dijkstra.shortestPath, graph, e, g)	
							  
if __name__=='__main__':
	if len(sys.argv) > 1:
		unittest.main(module=None)
	else:
		unittest.main()
		