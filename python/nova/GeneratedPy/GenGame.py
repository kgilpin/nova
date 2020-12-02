'''
GenGame.py
Tue Mar 29 11:44:59 2005
Generated by MiddleKit.
'''

# MK attribute caches for setFoo() methods
_timeCompressionAttr = None
_lastActionTimeAttr = None
_eventCounterAttr = None
_startTimeAttr = None
_endTimeAttr = None
_deathProbeCostAttr = None
_spyProbeCostAttr = None
_factoryCostAttr = None
_speedCostAttr = None
_battlePowerCostAttr = None
_rangeCostAttr = None
_probeShieldCostAttr = None
_deathShieldCostAttr = None
_nameAttr = None

import types
from mx import DateTime


from MiddleKit.Run.MiddleObject import MiddleObject
from types import InstanceType, LongType
from MiddleKit.Run.SQLObjectStore import ObjRefError



class GenGame(MiddleObject):

	def __init__(self):
		MiddleObject.__init__(self)
		self._timeCompression = 1.0
		self._lastActionTime  = None
		self._eventCounter    = 0
		self._startTime       = None
		self._endTime         = None
		self._deathProbeCost  = 200
		self._spyProbeCost    = 10
		self._factoryCost     = 5
		self._speedCost       = 500
		self._battlePowerCost = 100
		self._rangeCost       = 100
		self._probeShieldCost = 10
		self._deathShieldCost = 200
		self._name            = None

	def construct(self, startTime, endTime):
		# Construct the Game with all the required attributes that do not have default values
		self.setStartTime( startTime )
		self.setEndTime( endTime )

	def timeCompression(self):
		return self._timeCompression

	def setTimeCompression(self, value):
		if value is not None:
			if type(value) in (types.IntType, types.LongType):
				value = float(value)
			elif type(value) is not types.FloatType:
				raise TypeError, 'expecting float type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._timeCompression
		self._timeCompression = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _timeCompressionAttr
			if _timeCompressionAttr is None:
				_timeCompressionAttr = self.klass().lookupAttr('timeCompression')
				if not _timeCompressionAttr.shouldRegisterChanges():
					_timeCompressionAttr = 0
			if _timeCompressionAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['timeCompression'] = _timeCompressionAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def lastActionTime(self):
		return self._lastActionTime

	def setLastActionTime(self, value):
		# have DateTime
		if value is not None:
			if type(value) is type(''):
				value = DateTime.DateTimeFrom(value)
			if type(value) is not DateTime.DateTimeType:
				raise TypeError, 'expecting datetime type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._lastActionTime
		self._lastActionTime = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _lastActionTimeAttr
			if _lastActionTimeAttr is None:
				_lastActionTimeAttr = self.klass().lookupAttr('lastActionTime')
				if not _lastActionTimeAttr.shouldRegisterChanges():
					_lastActionTimeAttr = 0
			if _lastActionTimeAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['lastActionTime'] = _lastActionTimeAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def eventCounter(self):
		return self._eventCounter

	def setEventCounter(self, value):
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._eventCounter
		self._eventCounter = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _eventCounterAttr
			if _eventCounterAttr is None:
				_eventCounterAttr = self.klass().lookupAttr('eventCounter')
				if not _eventCounterAttr.shouldRegisterChanges():
					_eventCounterAttr = 0
			if _eventCounterAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['eventCounter'] = _eventCounterAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def startTime(self):
		return self._startTime

	def setStartTime(self, value):
		assert value is not None
		# have DateTime
		if value is not None:
			if type(value) is type(''):
				value = DateTime.DateTimeFrom(value)
			if type(value) is not DateTime.DateTimeType:
				raise TypeError, 'expecting datetime type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._startTime
		self._startTime = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _startTimeAttr
			if _startTimeAttr is None:
				_startTimeAttr = self.klass().lookupAttr('startTime')
				if not _startTimeAttr.shouldRegisterChanges():
					_startTimeAttr = 0
			if _startTimeAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['startTime'] = _startTimeAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def endTime(self):
		return self._endTime

	def setEndTime(self, value):
		assert value is not None
		# have DateTime
		if value is not None:
			if type(value) is type(''):
				value = DateTime.DateTimeFrom(value)
			if type(value) is not DateTime.DateTimeType:
				raise TypeError, 'expecting datetime type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._endTime
		self._endTime = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _endTimeAttr
			if _endTimeAttr is None:
				_endTimeAttr = self.klass().lookupAttr('endTime')
				if not _endTimeAttr.shouldRegisterChanges():
					_endTimeAttr = 0
			if _endTimeAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['endTime'] = _endTimeAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def deathProbeCost(self):
		return self._deathProbeCost

	def setDeathProbeCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._deathProbeCost
		self._deathProbeCost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _deathProbeCostAttr
			if _deathProbeCostAttr is None:
				_deathProbeCostAttr = self.klass().lookupAttr('deathProbeCost')
				if not _deathProbeCostAttr.shouldRegisterChanges():
					_deathProbeCostAttr = 0
			if _deathProbeCostAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['deathProbeCost'] = _deathProbeCostAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def spyProbeCost(self):
		return self._spyProbeCost

	def setSpyProbeCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._spyProbeCost
		self._spyProbeCost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _spyProbeCostAttr
			if _spyProbeCostAttr is None:
				_spyProbeCostAttr = self.klass().lookupAttr('spyProbeCost')
				if not _spyProbeCostAttr.shouldRegisterChanges():
					_spyProbeCostAttr = 0
			if _spyProbeCostAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['spyProbeCost'] = _spyProbeCostAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def factoryCost(self):
		return self._factoryCost

	def setFactoryCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._factoryCost
		self._factoryCost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _factoryCostAttr
			if _factoryCostAttr is None:
				_factoryCostAttr = self.klass().lookupAttr('factoryCost')
				if not _factoryCostAttr.shouldRegisterChanges():
					_factoryCostAttr = 0
			if _factoryCostAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['factoryCost'] = _factoryCostAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def speedCost(self):
		return self._speedCost

	def setSpeedCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._speedCost
		self._speedCost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _speedCostAttr
			if _speedCostAttr is None:
				_speedCostAttr = self.klass().lookupAttr('speedCost')
				if not _speedCostAttr.shouldRegisterChanges():
					_speedCostAttr = 0
			if _speedCostAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['speedCost'] = _speedCostAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def battlePowerCost(self):
		return self._battlePowerCost

	def setBattlePowerCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._battlePowerCost
		self._battlePowerCost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _battlePowerCostAttr
			if _battlePowerCostAttr is None:
				_battlePowerCostAttr = self.klass().lookupAttr('battlePowerCost')
				if not _battlePowerCostAttr.shouldRegisterChanges():
					_battlePowerCostAttr = 0
			if _battlePowerCostAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['battlePowerCost'] = _battlePowerCostAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def rangeCost(self):
		return self._rangeCost

	def setRangeCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._rangeCost
		self._rangeCost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _rangeCostAttr
			if _rangeCostAttr is None:
				_rangeCostAttr = self.klass().lookupAttr('rangeCost')
				if not _rangeCostAttr.shouldRegisterChanges():
					_rangeCostAttr = 0
			if _rangeCostAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['rangeCost'] = _rangeCostAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def probeShieldCost(self):
		return self._probeShieldCost

	def setProbeShieldCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._probeShieldCost
		self._probeShieldCost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _probeShieldCostAttr
			if _probeShieldCostAttr is None:
				_probeShieldCostAttr = self.klass().lookupAttr('probeShieldCost')
				if not _probeShieldCostAttr.shouldRegisterChanges():
					_probeShieldCostAttr = 0
			if _probeShieldCostAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['probeShieldCost'] = _probeShieldCostAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def deathShieldCost(self):
		return self._deathShieldCost

	def setDeathShieldCost(self, value):
		assert value is not None
		if value is not None:
			if type(value) is types.LongType:
				value = int(value)
			elif type(value) is not types.IntType:
				raise TypeError, 'expecting int type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._deathShieldCost
		self._deathShieldCost = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _deathShieldCostAttr
			if _deathShieldCostAttr is None:
				_deathShieldCostAttr = self.klass().lookupAttr('deathShieldCost')
				if not _deathShieldCostAttr.shouldRegisterChanges():
					_deathShieldCostAttr = 0
			if _deathShieldCostAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['deathShieldCost'] = _deathShieldCostAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)

	def name(self):
		return self._name

	def setName(self, value):
		if value is not None:
			if type(value) is not types.StringType:
				raise TypeError, 'expecting string type, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._name
		self._name = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _nameAttr
			if _nameAttr is None:
				_nameAttr = self.klass().lookupAttr('name')
				if not _nameAttr.shouldRegisterChanges():
					_nameAttr = 0
			if _nameAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['name'] = _nameAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)
