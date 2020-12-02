
class Star:
	def __init__(self):
		self._id = None
		self._name = None
		self._x = None
		self._y = None
		self._isDead = None
		self._owner = None
		self._ownerInfo = None
		
	def construct(self, id, name, x, y, isDead, owner, ownerInfo):
		"""
		owner is a Player
		ownerInfo is populated only if the player requesting the data is the owner of the star
		"""
		self._id = id
		self._name = name
		self._x = x
		self._y = y
		self._isDead = isDead
		self._owner = owner
		self._ownerInfo = ownerInfo
		if ownerInfo:
			ownerInfo._star = self
		return self

	def id(self): return self._id
	def name(self): return self._name
	def x(self): return self._x
	def y(self): return self._y
	def isDead(self): return self._isDead
	def owner(self): return self._owner
	def ownerInfo(self): return self._ownerInfo

	def __str__(self):
		props = "x,y : ( %d,%d )" % ( self.x(), self.y() )
		if self.ownerInfo():
			props = "%s, %s" % ( props, str(self.ownerInfo()) )
		return "%s [%s]" % ( self.name(), props )
		
		
class StarOwnerInfo:
	def __init__(self):
		self._wealth = None
		self._numShips = None
		self._numFactories = None
		self._hasProbeShield = None
		self._hasNovaShield = None
		self._star = None
	
	def construct(self, wealth, numShips, numFactories, hasProbeShield, hasNovaShield):
		"""
		numShips is the number of available ships on the star; the total minus the ones scheduled to leave
		"""
		self._wealth = wealth
		self._numShips = numShips
		self._numFactories = numFactories
		self._hasProbeShield = hasProbeShield
		self._hasNovaShield = hasNovaShield
		# Set by Star.construct
		self._star = None
		return self
		
	def wealth(self): return self._wealth
	def numShips(self): return self._numShips
	def numFactories(self): return self._numFactories
	def hasProbeShield(self): return self._hasProbeShield
	def hasNovaShield(self): return self._hasNovaShield
	def star(self): return self._star
	
	def __str__(self):
		return "wealth : %d, numShips : %d, numFactories : %d, hasProbeShield : %d, hasNovaShield : %d" % \
			   ( self.wealth(), self.numShips(), self.numFactories(), self.hasProbeShield(), self.hasNovaShield() )
		
