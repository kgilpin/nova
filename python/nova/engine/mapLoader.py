
# Uses the Python Image Library (PIL)
# http://www.pythonware.com/products/pil/index.htm
import Image
import sys

import log4py

Log = None

class StarMap:
	def __init__(self):
		self._stars = []
		self._isHomeWorld = {}
	
	def addStar(self, position, isHomeWorld):
		"""
		Position is an ( x, y ) tuple
		"""
		if isHomeWorld:
			Log.debug( 'Adding home world at ( %s, %s )' % position )
		else:
			Log.debug( 'Adding star at ( %s, %s )' % position )
		
		self._isHomeWorld[position] = isHomeWorld
		self._stars.append(position)

	def starData(self):
		return self._stars

	def isHomeWorld(self, starData):
		return self._isHomeWorld[starData]

	def __str__(self):
		return str(self._stars)

class MapLoader:
	def loadStarMap(self):
		""" Return a new StarMap, loaded from the initialization data provided """
		raise 'AbstractMethodError'

class ImageMapLoader(MapLoader):
	"""
	Loads a star map from an image. White pixels represent empty space, black pixels are
	stars, blue pixes are home worlds
	"""

	def __init__(self, imageFile):
		self._image = Image.open(imageFile)

	def loadStarMap(self):
		xlow, ylow, xhigh, yhigh = self._image.getbbox()

		map = StarMap()
		for x in range(xlow, xhigh):
			for y in range(ylow, yhigh):
				pixel = self._image.getpixel(( x, y ))
				r, g, b = pixel
				if pixel != ( 255, 255, 255 ):
					position = ( x, y )
					isHomeWorld = 0
					if b > r and b > g:
						isHomeWorld = 1
					map.addStar(position, isHomeWorld)
		return map

Log = log4py.Logger().get_instance(MapLoader)

if __name__ == "__main__":
	if not sys.argv[1:]:
		print "Syntax: python mapLoader.py fileName"
		sys.exit(1)

	print 'Loading %s' % sys.argv[1]
	loader = ImageMapLoader(sys.argv[1])
	loader.loadStarMap()
