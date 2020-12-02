
class Event:
	def __init__(self):
		self._executionTime = None
		self._client = None
		
	def construct(self, executionTime):
		self._executionTime = executionTime
		# Must be set externally
		self._client = None
		return self
		
	def executionTime(self): return self._executionTime
	def client(self): return self._client

	def __str__(self):
		" By default, __str__ is uiDescription "
		return self.uiDescription()

class ProductionEvent(Event):
	def __init__(self):
		Event.__init__(self)
		self._numShips = None
		self._cash = None

	def construct(self, executionTime, numShips, cash):
		Event.construct(self, executionTime)
		self._numShips = numShips
		self._cash = cash
		return self

	def numShips(self): return self._numShips
	def cash(self): return self._cash

	def uiDescription(self):
		"""
		Returns a description of how many ships were produced for the player
		"""
		return "Your stars produced <unit qty=%d /> and %d cash" % ( self.numShips(), self.cash() )

class StarEvent(Event):
	def __init__(self):
		Event.__init__(self)
		self._star = None
		
	def construct(self, executionTime, star):
		Event.construct(self, executionTime)
		self._star = star
		return self

	def star(self): return self._star

class BattleEvent(StarEvent):
	def __init__(self):
		StarEvent.__init__(self)
		self._attacker = None
		self._defender = None
		self._victor = None
		self._battleInfo = None
		
	def construct(self, executionTime, star, attacker, defender, victor, battleInfo):
		"""
		attacker, defender, and victor are Player objects
		battleInfo is available if the requesting player is the attacker or defender
		"""
		StarEvent.construct(self, executionTime, star)
		self._attacker = attacker
		self._defender = defender
		self._victor = victor
		self._battleInfo = battleInfo
		if battleInfo:
			battleInfo._battle = self
		return self

	def attacker(self): return self._attacker
	def defender(self): return self._defender
	def victor(self): return self._victor
	def battleInfo(self): return self._battleInfo

	def uiDescription(self):
		if self.client() is self.defender():
			if self.victor() is self.attacker():
				winner = self.attacker().name()
			else:
				winner = "You"
			return "<color>%s attacked <star name=%s/> with <unit qty=%d />!</color><br/>" \
				   "You had <unit qty=%d /> stationed there at the time<br/>" \
				   "%s won the battle, with <unit qty=%d /> remaining" % \
				   ( self.attacker().name(), self.star().name(), self.battleInfo().numAttackingShips(),
					 self.battleInfo().numDefendingShips(), winner, self.battleInfo().numShipsRemaining() )
		elif self.client() is self.attacker():
			if self.victor() is self.attacker():
				winner = "You"
			else:
				winner = self.defender().name()
			return "<unit qty=%d /> attacked <star name=%s/> (owner %s, <unit qty=%d />)<br/>" \
				   "%s won the battle, with <unit qty=%d /> remaining" % \
				   ( self.battleInfo().numAttackingShips(), self.star().name(), self.defender().name(), self.battleInfo().numDefendingShips(),
					 winner, self.battleInfo().numShipsRemaining() )
		elif self.victor() is self.attacker():
			return "<i>%s captured <star name=%s/> (from %s)</i>" % ( self.victor().name(), self.star().name(), self.defender().name() )

class ParticipantBattleInfo:
	def __init__(self):
		self._numAttackingShips = None
		self._numDefendingShips = None
		self._victorShipsRemaining = None
		self._battle = None
		
	def construct(self, numAttackingShips, numDefendingShips, victorShipsRemaining):
		self._numAttackingShips = numAttackingShips
		self._numDefendingShips = numDefendingShips
		self._victorShipsRemaining = victorShipsRemaining
		self._battle = None
		return self
		
	def numAttackingShips(self): return self._numAttackingShips
	def numDefendingShips(self): return self._numDefendingShips
	def victorShipsRemaining(self): return self._victorShipsRemaining
	def numShipsRemaining(self): return self.victorShipsRemaining()
	def battle(self): return self._battle
	
class ArrivalEvent(StarEvent):
	def __init__(self):
		StarEvent.__init__(self)
		self._origin = None
		self._finalDestination = None
		self._numShips = None
		
	def construct(self, executionTime, destination, finalDestination, origin, numShips):
		StarEvent.construct(self, executionTime, destination)
		self._origin = origin
		self._finalDestination = finalDestination
		self._numShips = numShips
		return self
		
	def destination(self): return self._star
	def finalDestination(self): return self._finalDestination
	def origin(self): return self._origin
	def numShips(self): return self._numShips

	def uiDescription(self):
		description = "<unit qty=%d /> arrived at <star name=%s/>" % ( self.numShips(), self.destination().name() )
		if self.finalDestination() is not None and self.finalDestination() is not self.destination():
			description += " on the way to <star name=%s/>" % self.finalDestination().name()
		return description

class FieryDeathEvent(StarEvent):
	def __init__(self):
		StarEvent.__init__(self)
		self._numShips = None
		
	def construct(self, executionTime, star, numShips):
		StarEvent.construct(self, executionTime, star)
		self._numShips = numShips
		return self

	def numShips(self): return self._numShips

	def uiDescription(self):
		return "<unit qty=%d /> died a fiery death emerging from hyperspace at the dead star <star name=%s/>" % \
			   ( self.numShips(), self.star().name() )

class NovaBombEvent(StarEvent):
	def __init__(self):
		StarEvent.__init__(self)
		self._hasDeathShield = None
		
	def construct(self, executionTime, star, hasDeathShield):
		"""
		If hasDeathShield is false, the star was destroyed
		"""
		StarEvent.construct(self, executionTime, star)
		self._hasDeathShield = hasDeathShield
		return self
	
	def hasDeathShield(self): return self._hasDeathShield

	def uiDescription(self):
		if not self.hasDeathShield():
			return "<color><b><star name=%s/> was destroyed by a nova bomb!</b></color>" % self.star().name()
		else:
			return "<color>The nova bomb sent to <star name=%s/> was blocked by a shield</color>" % self.star().name()

class ProbeEvent(StarEvent):
	def __init__(self):
		StarEvent.__init__(self)
		self._sender = None
		self._owner = None
		self._hasProbeShield = None
		self._starInfo = None
		
	def construct(self, executionTime, star, sender, owner, hasProbeShield, starInfo):
		"""
		starInfo is None if hasProbeShield is true
		"""
		StarEvent.construct(self, executionTime, star)
		self._sender = sender
		self._owner = owner
		self._hasProbeShield = hasProbeShield
		self._starInfo = starInfo
		if starInfo:
			starInfo._star = star
		return self

	def sender(self): return self._sender
	def owner(self): return self._owner
	def hasProbeShield(self): return self._hasProbeShield
	def starInfo(self): return self._starInfo

	def uiDescription(self):
		if self.client() is self.sender():
			description = "<color>Probe Report: <star name=%s/></color><br/>" % self.star().name()
			if not self.hasProbeShield():
				if self.starInfo().hasNovaShield():
					novaShield = "Yes"
				else:
					novaShield = "No"
				if self.starInfo().hasProbeShield():
					probeShield = "Yes"
				else:
					probeShield = "No"
				description += "Owner:%s, Wealth:%d, Factories:%d, Ships:%d, Nova Shield:%s, Probe Shield:%s" % \
							   ( self.owner().name(), self.starInfo().wealth(), self.starInfo().numFactories(), self.starInfo().numShips(), \
								 novaShield, probeShield )
			else:
				description += "The probe's transmission was blocked by a shield"
			return description
		else:
			if self.hasProbeShield():
				return "<color>Your probe shield at <star name=%s/> blocked a probe!</color>" % self.star().name()
		return ""


