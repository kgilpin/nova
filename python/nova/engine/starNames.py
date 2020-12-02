import os

from xml.sax import parse, ContentHandler

class StarHandler(ContentHandler):
	"""
	Saves the content from the <name> and <mag> elements in the star name data
	"""
	def __init__(self):
		self._stars = []
		
	def stars(self):
		"""
		Returns a list of ( name, mag ) tuples
		"""
		return self._stars
	
	def startElement(self, name, attrs):
		self._element = name
		if name == 'star':
			self._name = None
			self._mag = None

	def endElement(self, name):
		if name == 'star':
			self._stars.append(( self._name, self._mag))

	def characters(self, content):
		if self._element == 'name':
			self._name = content
		elif self._element == 'mag':
			self._mag = content
			
class StarParser:
	def __init__(self):
		dir = os.path.dirname(__file__)
		fileName = os.path.join(os.path.abspath(dir), 'starNames.xml')
		handler = StarHandler()
		parse(fileName, handler)
		self._stars = handler.stars()
		
	def stars(self):
		return self._stars

