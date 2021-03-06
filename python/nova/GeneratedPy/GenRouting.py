'''
GenRouting.py
Tue Mar 29 11:44:59 2005
Generated by MiddleKit.
'''

# MK attribute caches for setFoo() methods
_gameAttr = None
_starAttr = None
_numShipsAttr = None
_percentAttr = None
_destinationAttr = None

import types
from mx import DateTime
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))))
from nova.StandingOrder import StandingOrder
del sys.path[0]

from types import InstanceType, LongType
from MiddleKit.Run.SQLObjectStore import ObjRefError



class GenRouting(StandingOrder):

	def __init__(self):
		StandingOrder.__init__(self)
		self._numShips    = 0
		self._percent     = 0.0
		self._destination = None

	def construct(self, game, star):
		# Construct the Routing with all the required attributes that do not have default values
		self.setGame( game )
		self.setStar( star )

	def numShips(self):
		return self._numShips

	def setNumShips(self, value):
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._numShips
		self._numShips = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _numShipsAttr
			if _numShipsAttr is None:
				_numShipsAttr = self.klass().lookupAttr('numShips')
				if not _numShipsAttr.shouldRegisterChanges():
					_numShipsAttr = 0
			if _numShipsAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['numShips'] = _numShipsAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def percent(self):
		return self._percent

	def setPercent(self, value):
		if value is not None:
			if type(value) in (types.IntType, types.LongType):
				value = float(value)
			elif type(value) is not types.FloatType:
				raise TypeError, 'expecting float type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._percent
		self._percent = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _percentAttr
			if _percentAttr is None:
				_percentAttr = self.klass().lookupAttr('percent')
				if not _percentAttr.shouldRegisterChanges():
					_percentAttr = 0
			if _percentAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['percent'] = _percentAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def destination(self):
		if self._destination is not None and type(self._destination) is not InstanceType:
			try:
				self.__dict__['_destination'] = self._mk_store.fetchObjRef(self._destination)
			except ObjRefError, e:
				self.__dict__['_destination'] = self.objRefErrorWasRaised(e, 'Routing', 'destination')
		return self._destination

	def setDestination(self, value):
		
		if value is not None and type(value) is not LongType:
			if not type(value) is InstanceType:
				raise TypeError, 'expecting InstanceType, but got value %r of type %r instead' % (value, type(value))
			from nova.Star import Star
			if not isinstance(value, Star):
				raise TypeError, 'expecting Star, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._destination
		self._destination = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _destinationAttr
			if _destinationAttr is None:
				_destinationAttr = self.klass().lookupAttr('destination')
				if not _destinationAttr.shouldRegisterChanges():
					_destinationAttr = 0
			if _destinationAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['destination'] = _destinationAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

