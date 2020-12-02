'''
GenGameObject.py
Tue Mar 29 11:44:59 2005
Generated by MiddleKit.
'''

# MK attribute caches for setFoo() methods
_gameAttr = None

import types
from mx import DateTime


from MiddleKit.Run.MiddleObject import MiddleObject
from types import InstanceType, LongType
from MiddleKit.Run.SQLObjectStore import ObjRefError



class GenGameObject(MiddleObject):

	def __init__(self):
		MiddleObject.__init__(self)
		self._game = None

	def construct(self, game):
		# Construct the GameObject with all the required attributes that do not have default values
		self.setGame( game )

	def game(self):
		if self._game is not None and type(self._game) is not InstanceType:
			try:
				self.__dict__['_game'] = self._mk_store.fetchObjRef(self._game)
			except ObjRefError, e:
				self.__dict__['_game'] = self.objRefErrorWasRaised(e, 'GameObject', 'game')
		return self._game

	def setGame(self, value):
		assert value is not None
		if value is not None and type(value) is not LongType:
			if not type(value) is InstanceType:
				raise TypeError, 'expecting InstanceType, but got value %r of type %r instead' % (value, type(value))
			from nova.Game import Game
			if not isinstance(value, Game):
				raise TypeError, 'expecting Game, but got value %r of type %r instead' % (value, type(value))

		# set the attribute
		origValue = self._game
		self._game = value

		# MiddleKit machinery
		self._mk_changed = 1  # @@ original semantics, but I think this should be under "if not self._mk_initing..."
		if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
			global _gameAttr
			if _gameAttr is None:
				_gameAttr = self.klass().lookupAttr('game')
				if not _gameAttr.shouldRegisterChanges():
					_gameAttr = 0
			if _gameAttr:
				# Record that it has been changed
				if self._mk_changedAttrs is None:
					self._mk_changedAttrs = {} # maps name to attribute
				self._mk_changedAttrs['game'] = _gameAttr  # changedAttrs is a set
				# Tell ObjectStore it happened
				self._mk_store.objectChanged(self)
