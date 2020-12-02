from __future__ import nested_scopes

import inspect, string, types

import nova
from nova.bean.star import Star
from nova.bean.player import Player
from nova.util.Log import log

from mx import DateTime
from MiddleKit.Run.MiddleObject import MiddleObject

def toUCC(str):
	if str is None or len(str) == 0:
		result = str
	else:
		result = string.upper(str[0]) + str[1:]
	return result

def toLCC(str):
	"""
	Convert the first character to lower-case, unless both of the first two characters
	are upper-case
	"""
	if len(str) > 1 and \
			 string.upper(str[0]) == str[0] and \
			 string.upper(str[1]) == str[1]:
		return str
	else:
		return string.lower(str[0]) + str[1:]

def isSetMethod(str):
	if str is None or len(str) < 4:
		result = 0
	else:
		result = str[0:3] == 'set' and string.upper(str[3]) == str[3]
	return result

class Marshal:
	"""
	Converts a Python object into an XML-RPC compatible data structure consisting of lists and maps
	"""

	def __init__(self):
		self._visitedObjects = {}

	def marshal(self, obj):
		result = None
		if type(obj) == type([]):
			result = []
			for item in obj:
				result.append( self.marshal(item) )
		else:
			result = self.marshalObject(obj)
		return result

	def unmarshal(self, data):
		result = None
		if type(data) == type([]):
			result = []
			for item in data:
				result.append( self.unmarshal(item) )
		else:
			result = self.unmarshalStruct(data)
		return result

	def marshalObject(self, obj):
		" Objects are marshalled into structs (maps)"
		
		self._visitedObjects[obj] = 1
		struct = { }

		if isinstance(obj, DateTime.DateTimeType):
			struct['__classname__'] = 'mx.DateTime.DateTime'
			struct['ticks'] = obj.ticks()
		else:
			struct['__classname__'] = str(obj.__class__)
			getMethods = self.findGetMethods(obj)
			for method in getMethods:
				name = method.__name__
				value = method(obj)
				log(name, " = ", value)
				if value is not None:
					if isinstance(value, types.InstanceType) and str(value.__class__).startswith('nova.bean.'):
						log("\t", name, " is a nova.bean")
						if not self._visitedObjects.has_key(value):
							result = self.marshal(value)
							struct[name] = result
						else:
							keyProperty, keyValue = None, None
							if str(value.__class__).endswith('Star'): # isinstance(value, Star):
								keyProperty, keyValue = 'id', value.id()
							elif str(value.__class__).endswith('Player'): #isinstance(value, Player):
								keyProperty, keyValue = 'name', value.name()
							else:
								raise 'Unexpected reference to %s %s' % ( value.__class__, value )
							struct[name] = { '__reference__' : 1, '__classname__' : str(value.__class__), \
											'keyProperty' : keyProperty, 'keyValue' : keyValue }
					elif isinstance(value, DateTime.DateTimeType) or isinstance(value, types.ListType):
						struct[name] = self.marshal(value)
					else:
						struct[name] = value
		return struct

	def unmarshalStruct(self, map):
		className = map['__classname__']
		if map.has_key('__reference__'):
			keyValue = map['keyValue']
			return self._visitedObjects[ ( className, keyValue ) ]
		else:
			if className == 'mx.DateTime.DateTime':
				ticks = map['ticks']
				obj = DateTime.TimestampFromTicks(ticks)
			else:
				packageName = className[:className.rindex('.')]
				exec('import %s' % packageName)
				exec('obj = %s()' % className)
				key = None
				if className == str(Star):
					key = ( str(Star), map['id'] )
				elif className == str(Player):
					key = ( str(Player), map['name'] )

				if key is not None:
					self._visitedObjects[key] = obj

				del map['__classname__']
				
				for attrName in self.sortAttrNames(map.keys()):
					value = map[attrName]
					if type(value) == type({}) or type(value) == type([]):
						value = self.unmarshal(value)
					setattr(obj, '_%s' % attrName, value)
			return obj

	def sortAttrNames(self, names):
		"""
		There is some load-order dependency in the attribute names. For instance, players should be loaded before
		stars so that the Star.owner property will resolve. Would be nice to not hard-code this, but this will do for now
		"""
		specialNames = [ 'players', 'stars' ]
		specialNames.reverse()
		for specialName in specialNames:
			if specialName in names:
				names.remove(specialName)
				names.insert(0, specialName)
		return names
	
	def findGetMethods(self, obj):
		"""
		Finds all 'get' methods by looking for corresponding members which begin with an underscore
		"""
		allMethods = inspect.getmembers(obj.__class__, inspect.ismethod)
		fields = dir( obj )
		# dir returns a list of data fields
		# inspect returns ( name, method ) pairs
		# method.im_func is the function that implements the method
		return map(lambda pair: pair[1], filter(lambda pair: '_%s' % pair[0] in fields, allMethods) )

	def findSettableFields(self, obj):
		"""
		Finds all settable fields by looking for '_foo' fields
		Returns a list of field names
		"""
		allMethods = inspect.getmembers(obj, inspect.ismethod)
		fields = dir( obj )
		# inspect returns ( name, method ) pairs
		# method.im_func is the function that implements the method
		# getargspec[0] is the tuple of function arguments
		return filter(lambda pair: '_%s' % pair[0] in fields, allMethods)

	def extends(self, candidate, searchFor):
		try:
			if searchFor in candidate.__bases__:
				return 1
			for base in candidate.__bases__:
				if self.extends(base, searchFor):
					return 1
		except:
			pass
		return 0

if __name__ == '__main__':
	from nova.bean.player import PlayerOwnerInfo
	kevinInfo = PlayerOwnerInfo().construct(0.5, 10, 150, 225)
	kevin = Player().construct('kevin', kevinInfo)
	s = Star().construct(0, 'Orion', 10, 12, 0, kevin, None)
	map = Marshal().marshal(s)
	
	print map
	
	s = Marshal().unmarshal(map)
	print s
	print s.owner()
	print s.ownerInfo()

	
	