'''
GenSpyProbeEvent.py
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
_ownerAttr = None
_wealthAttr = None
_numShipsAttr = None
_numFactoriesAttr = None
_hasSpyShieldAttr = None
_hasDeathShieldAttr = None

import types
from mx import DateTime
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))))
from nova.Event import Event
del sys.path[0]

from types import InstanceType, LongType
from MiddleKit.Run.SQLObjectStore import ObjRefError



class GenSpyProbeEvent(Event):

	def __init__(self):
		Event.__init__(self)
		self._star           = None
		self._owner          = None
		self._wealth         = 0
		self._numShips       = 0
		self._numFactories   = 0
		self._hasSpyShield   = None
		self._hasDeathShield = 0

	def construct(self, game, executionTime, player, star, owner):
		# Construct the SpyProbeEvent with all the required attributes that do not have default values
		self.setGame( game )
		self.setExecutionTime( executionTime )
		self.setPlayer( player )
		self.setStar( star )
		self.setOwner( owner )

	def star(self):
		if self._star is not None and type(self._star) is not InstanceType:
			try:
				self.__dict__['_star'] = self._mk_store.fetchObjRef(self._star)
			except ObjRefError, e:
				self.__dict__['_star'] = self.objRefErrorWasRaised(e, 'SpyProbeEvent', 'star')
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

	def owner(self):
		if self._owner is not None and type(self._owner) is not InstanceType:
			try:
				self.__dict__['_owner'] = self._mk_store.fetchObjRef(self._owner)
			except ObjRefError, e:
				self.__dict__['_owner'] = self.objRefErrorWasRaised(e, 'SpyProbeEvent', 'owner')
		return self._owner

	def setOwner(self, value):
		assert value is not None
		if value is not None and type(value) is not LongType:
			if not type(value) is InstanceType:
				raise TypeError, 'expecting InstanceType, but got value %r of type %r instead' % (value, type(value))
			from nova.Player import Player
			if not isinstance(value, Player):
				raise TypeError, 'expecting Player, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._owner
		self._owner = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _ownerAttr
			if _ownerAttr is None:
				_ownerAttr = self.klass().lookupAttr('owner')
				if not _ownerAttr.shouldRegisterChanges():
					_ownerAttr = 0
			if _ownerAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['owner'] = _ownerAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def wealth(self):
		return self._wealth

	def setWealth(self, value):
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

	def numFactories(self):
		return self._numFactories

	def setNumFactories(self, value):
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._numFactories
		self._numFactories = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _numFactoriesAttr
			if _numFactoriesAttr is None:
				_numFactoriesAttr = self.klass().lookupAttr('numFactories')
				if not _numFactoriesAttr.shouldRegisterChanges():
					_numFactoriesAttr = 0
			if _numFactoriesAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['numFactories'] = _numFactoriesAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def hasSpyShield(self):
		return self._hasSpyShield

	def setHasSpyShield(self, value):
		if value is not None:
			if type(value) is not types.IntType:
				raise TypeError, 'expecting int for bool, but got value %r of type %r instead' % (value, type(value))
			if value not in (0, 1):
				raise ValueError, 'expecting 0 or 1 for bool, but got %s instead' % value

		# set the attribute
		origValue = self._hasSpyShield
		self._hasSpyShield = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _hasSpyShieldAttr
			if _hasSpyShieldAttr is None:
				_hasSpyShieldAttr = self.klass().lookupAttr('hasSpyShield')
				if not _hasSpyShieldAttr.shouldRegisterChanges():
					_hasSpyShieldAttr = 0
			if _hasSpyShieldAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['hasSpyShield'] = _hasSpyShieldAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def hasDeathShield(self):
		return self._hasDeathShield

	def setHasDeathShield(self, value):
		if value is not None:
			if type(value) is not types.IntType:
				raise TypeError, 'expecting int for bool, but got value %r of type %r instead' % (value, type(value))
			if value not in (0, 1):
				raise ValueError, 'expecting 0 or 1 for bool, but got %s instead' % value

		# set the attribute
		origValue = self._hasDeathShield
		self._hasDeathShield = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _hasDeathShieldAttr
			if _hasDeathShieldAttr is None:
				_hasDeathShieldAttr = self.klass().lookupAttr('hasDeathShield')
				if not _hasDeathShieldAttr.shouldRegisterChanges():
					_hasDeathShieldAttr = 0
			if _hasDeathShieldAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['hasDeathShield'] = _hasDeathShieldAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

