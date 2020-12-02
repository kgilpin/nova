'''
GenPurchaseEvent.py
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

import types
from mx import DateTime
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))))
from nova.Event import Event
del sys.path[0]

from types import InstanceType, LongType
from MiddleKit.Run.SQLObjectStore import ObjRefError



class GenPurchaseEvent(Event):

	def __init__(self):
		Event.__init__(self)
		self._cost = None

	def construct(self, game, executionTime, player, cost):
		# Construct the PurchaseEvent with all the required attributes that do not have default values
		self.setGame( game )
		self.setExecutionTime( executionTime )
		self.setPlayer( player )
		self.setCost( cost )

	def cost(self):
		return self._cost

	def setCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) in (types.IntType, types.LongType):
				value = float(value)
			elif type(value) is not types.FloatType:
				raise TypeError, 'expecting float type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._cost
		self._cost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _costAttr
			if _costAttr is None:
				_costAttr = self.klass().lookupAttr('cost')
				if not _costAttr.shouldRegisterChanges():
					_costAttr = 0
			if _costAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['cost'] = _costAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

