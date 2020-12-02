'''
GenCreateRoutingEvent.py
Tue Mar 29 11:44:59 2005
Generated by MiddleKit.
'''

# MK attribute caches for setFoo() methods
_gameAttr = None
_executionTimeAttr = None
_eventCounterAttr = None
_playerAttr = None
_statusAttr = None
_originAttr = None
_destinationAttr = None
_garrisonAttr = None

import types
from mx import DateTime
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))))
from nova.Event import Event
del sys.path[0]

from types import InstanceType, LongType
from MiddleKit.Run.SQLObjectStore import ObjRefError



class GenCreateRoutingEvent(Event):

	def __init__(self):
		Event.__init__(self)
		self._origin      = None
		self._destination = None
		self._garrison    = None

	def construct(self, game, executionTime, player, origin, destination, garrison):
		# Construct the CreateRoutingEvent with all the required attributes that do not have default values
		self.setGame( game )
		self.setExecutionTime( executionTime )
		self.setPlayer( player )
		self.setOrigin( origin )
		self.setDestination( destination )
		self.setGarrison( garrison )

	def origin(self):
		if self._origin is not None and type(self._origin) is not InstanceType:
			try:
				self.__dict__['_origin'] = self._mk_store.fetchObjRef(self._origin)
			except ObjRefError, e:
				self.__dict__['_origin'] = self.objRefErrorWasRaised(e, 'CreateRoutingEvent', 'origin')
		return self._origin

	def setOrigin(self, value):
		assert value is not None
		if value is not None and type(value) is not LongType:
			if not type(value) is InstanceType:
				raise TypeError, 'expecting InstanceType, but got value %r of type %r instead' % (value, type(value))
			from nova.Star import Star
			if not isinstance(value, Star):
				raise TypeError, 'expecting Star, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._origin
		self._origin = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _originAttr
			if _originAttr is None:
				_originAttr = self.klass().lookupAttr('origin')
				if not _originAttr.shouldRegisterChanges():
					_originAttr = 0
			if _originAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['origin'] = _originAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def destination(self):
		if self._destination is not None and type(self._destination) is not InstanceType:
			try:
				self.__dict__['_destination'] = self._mk_store.fetchObjRef(self._destination)
			except ObjRefError, e:
				self.__dict__['_destination'] = self.objRefErrorWasRaised(e, 'CreateRoutingEvent', 'destination')
		return self._destination

	def setDestination(self, value):
		assert value is not None
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

	def garrison(self):
		return self._garrison

	def setGarrison(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._garrison
		self._garrison = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _garrisonAttr
			if _garrisonAttr is None:
				_garrisonAttr = self.klass().lookupAttr('garrison')
				if not _garrisonAttr.shouldRegisterChanges():
					_garrisonAttr = 0
			if _garrisonAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['garrison'] = _garrisonAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

