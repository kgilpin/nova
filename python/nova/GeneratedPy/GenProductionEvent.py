'''
GenProductionEvent.py
Tue Mar 29 11:44:59 2005
Generated by MiddleKit.
'''

# MK attribute caches for setFoo() methods
_gameAttr = None
_executionTimeAttr = None
_eventCounterAttr = None
_playerAttr = None
_statusAttr = None
_starAttr = None
_numShipsAttr = None
_wealthAttr = None
_globalProductionEventAttr = None

import types
from mx import DateTime
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))))
from nova.Event import Event
del sys.path[0]

from types import InstanceType, LongType
from MiddleKit.Run.SQLObjectStore import ObjRefError



class GenProductionEvent(Event):

	def __init__(self):
		Event.__init__(self)
		self._star                  = None
		self._numShips              = None
		self._wealth                = None
		self._globalProductionEvent = None

	def construct(self, game, executionTime, player, star, numShips, wealth, globalProductionEvent):
		# Construct the ProductionEvent with all the required attributes that do not have default values
		self.setGame( game )
		self.setExecutionTime( executionTime )
		self.setPlayer( player )
		self.setStar( star )
		self.setNumShips( numShips )
		self.setWealth( wealth )
		self.setGlobalProductionEvent( globalProductionEvent )

	def star(self):
		if self._star is not None and type(self._star) is not InstanceType:
			try:
				self.__dict__['_star'] = self._mk_store.fetchObjRef(self._star)
			except ObjRefError, e:
				self.__dict__['_star'] = self.objRefErrorWasRaised(e, 'ProductionEvent', 'star')
		return self._star

	def setStar(self, value):
		assert value is not None
		if value is not None and type(value) is not LongType:
			if not type(value) is InstanceType:
				raise TypeError, 'expecting InstanceType, but got value %r of type %r instead' % (value, type(value))
			from nova.Star import Star
			if not isinstance(value, Star):
				raise TypeError, 'expecting Star, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._star
		self._star = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _starAttr
			if _starAttr is None:
				_starAttr = self.klass().lookupAttr('star')
				if not _starAttr.shouldRegisterChanges():
					_starAttr = 0
			if _starAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['star'] = _starAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def numShips(self):
		return self._numShips

	def setNumShips(self, value):
		assert value is not None
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

	def wealth(self):
		return self._wealth

	def setWealth(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._wealth
		self._wealth = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _wealthAttr
			if _wealthAttr is None:
				_wealthAttr = self.klass().lookupAttr('wealth')
				if not _wealthAttr.shouldRegisterChanges():
					_wealthAttr = 0
			if _wealthAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['wealth'] = _wealthAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def globalProductionEvent(self):
		if self._globalProductionEvent is not None and type(self._globalProductionEvent) is not InstanceType:
			try:
				self.__dict__['_globalProductionEvent'] = self._mk_store.fetchObjRef(self._globalProductionEvent)
			except ObjRefError, e:
				self.__dict__['_globalProductionEvent'] = self.objRefErrorWasRaised(e, 'ProductionEvent', 'globalProductionEvent')
		return self._globalProductionEvent

	def setGlobalProductionEvent(self, value):
		assert value is not None
		if value is not None and type(value) is not LongType:
			if not type(value) is InstanceType:
				raise TypeError, 'expecting InstanceType, but got value %r of type %r instead' % (value, type(value))
			from nova.GlobalProductionEvent import GlobalProductionEvent
			if not isinstance(value, GlobalProductionEvent):
				raise TypeError, 'expecting GlobalProductionEvent, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._globalProductionEvent
		self._globalProductionEvent = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _globalProductionEventAttr
			if _globalProductionEventAttr is None:
				_globalProductionEventAttr = self.klass().lookupAttr('globalProductionEvent')
				if not _globalProductionEventAttr.shouldRegisterChanges():
					_globalProductionEventAttr = 0
			if _globalProductionEventAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['globalProductionEvent'] = _globalProductionEventAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)
