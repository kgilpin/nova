'''
BattleEvent.py
'''

import log4py

from Event import Event
from GeneratedPy.GenBattleEvent import GenBattleEvent
from nova.bean import event

import random

"""
Use this variable for testing purposes to specify the sequence of 'random' numbers that
will be used to determine the outcome of the battle. The 'sequence' object should be a function
"""
randomSequence = None
Log = None

class Message:
	def __init__(self, *args):
		self._args = args

	def __str__(self):
		return reduce(lambda x, y: "%s%s" % ( x, y ), self._args)

def nextRandom():
	Log.debug(Message('randomSequence is ', randomSequence))
	if randomSequence is not None:
		return randomSequence()
	else:
		return random.random()

class BattleEvent(GenBattleEvent):
	def createBean(self, beanContext):
		"""
		Construct a BattleEvent bean
		beanContext is an instance of nova.beanContext.BeanContext
		"""
		battleInfo = None
		if self.defender() is beanContext.client() or self.attacker() is beanContext.client():
			battleInfo = event.ParticipantBattleInfo().construct(self.numAttackingShips(), self.numDefendingShips(), self.numShipsRemaining())
		return beanContext.addEvent( event.BattleEvent().construct(self.executionTime(), beanContext.star(self.star()),
																   beanContext.player(self.attacker()), beanContext.player(self.defender()),
																   beanContext.player(self.victor()), battleInfo) )
	
	def numShipsRemaining(self):
		"""
		Get the number of ships which remain to the victor
		"""
		if self.victor() is self.attacker():
			return self.numAttackingShips() - self.numShipsLost()
		else:
			return self.numDefendingShips() - self.numShipsLost()		

	def construct(self, game, executionTime, player, star, attacker, defender, numAttackingShips):
		numDefendingShips = star.numShips()

		attackingShips = numAttackingShips
		defendingShips = numDefendingShips
		while attackingShips > 0 and defendingShips > 0:
			# Apply the magic formula to compute the outcome of the battle
			# The odds start out 60-40 in favor of the defender
			# If the attacker has 50% or more ships, the odds are 50/50
			# If the defender has 50% or more ships, the odds are 70/30
			# Each player's chances are multiplied by his battle power
			# Ties always go to the defender

			if attackingShips > defendingShips * 1.5:
				attackPower = 50.0
				defendPower = 50.0
			elif defendingShips > attackingShips * 1.5:
				attackPower = 30.0
				defendPower = 70.0
			else:
				attackPower = 40.0
				defendPower = 60.0
				
			attackPower *= attacker.battlePower() / 100.0
			defendPower *= defender.battlePower() / 100.0

			Log.debug(Message('attackPower : ', attackPower, ', defendPower : ', defendPower))

			defenderOdds = defendPower / ( defendPower + attackPower )
			outcome = nextRandom()

			Log.debug(Message('\tdefenderOdds : ', defenderOdds, ', outcome : ', outcome))
				
			if outcome <= defenderOdds:
				attackingShips -= 1
			else:
				defendingShips -= 1
			
		victor = None
		numShipsLost = 0
		if attackingShips <= 0:
			victor = defender
			numShipsLost = numDefendingShips - defendingShips
		else:
			victor = attacker
			numShipsLost = numAttackingShips - attackingShips
		
		GenBattleEvent.construct(self, game, executionTime, player, star, attacker, defender, victor,
										 numAttackingShips, numDefendingShips, numShipsLost)

	def execute(self):
		"""
		If the attacker won
		o replace the owner of destination star
		o land all his ships on the destination star
		Else
		o subtract the numShipsLost from the number of ships on the star
		"""
		if self.victor() is self.attacker():
			self.star().setOwner( self.victor() )
			self.star().setNumShips( self.numAttackingShips() - self.numShipsLost() )
		else:
			self.star().subtractShips( self.numShipsLost() )

Log = log4py.Logger().get_instance(BattleEvent)
