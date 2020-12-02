'''
GenPurchaseBattlePowerEvent.py
Tue Mar 29 11:44:59 2005
Generated by MiddleKit.
'''

# MK attribute caches for setFoo() methods
_gameAttr = None
_executionTimeAttr = None
_eventCounterAttr = None
_playerAttr = None
_statusAttr = None
_costAttr = None
_deltaAttr = None

import types
from mx import DateTime
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))))
from nova.PurchaseEvent import PurchaseEvent
del sys.path[0]

from types import InstanceType, LongType
from MiddleKit.Run.SQLObjectStore import ObjRefError



class GenPurchaseBattlePowerEvent(PurchaseEvent):

	def __init__(self):
		PurchaseEvent.__init__(self)
		self._delta = None

	def construct(self, game, executionTime, player, cost, delta):
		# Construct the PurchaseBattlePowerEvent with all the required attributes that do not have default values
		self.setGame( game )
		self.setExecutionTime( executionTime )
		self.setPlayer( player )
		self.setCost( cost )
		self.setDelta( delta )

	def delta(self):
		return self._delta

	def setDelta(self, value):
		assert value is not None
		if value is not None:
			if type(value) in (types.IntType, types.LongType):
				value = float(value)
			elif type(value) is not types.FloatType:
				raise TypeError, 'expecting float type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._delta
		self._delta = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _deltaAttr
			if _deltaAttr is None:
				_deltaAttr = self.klass().lookupAttr('delta')
				if not _deltaAttr.shouldRegisterChanges():
					_deltaAttr = 0
			if _deltaAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['delta'] = _deltaAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

