
class Player:
	"""
	Represents a participant in the game. If the Player represents the player who is
	using the API, then ownerInfo will be populated. Otherwise it is None
	"""
	def __init__(self):
		self._name = None
		self._ownerInfo = None
	
	def construct(self, name, ownerInfo = None):
		self._name	= name
		self._ownerInfo = ownerInfo
		if ownerInfo:
			ownerInfo._player = self
		return self

	def name(self): return self._name
	def ownerInfo(self): return self._ownerInfo
	
	def __str__(self):
		if self.ownerInfo():
			return "%s [ %s ]" % ( self.name(), str(self.ownerInfo()) )
		else:
			return self.name()

class PlayerOwnerInfo:
	def __init__(self):
		self._player = None
		self._speed = None
		self._range = None
		self._income = None
		self._cash = None
		
	def construct(self, speed, range, income, cash):
		# self.player is be populated by Player.construct
		self._player = None
		self._speed = speed
		self._range = range
		self._income = income
		self._cash = cash
		return self
		
	def speed(self): return self._speed
	def range(self): return self._range
	def income(self): return self._income
	def cash(self): return self._cash
	def player(self): return self._player
	
	def __str__(self):
		return "speed : %.2f, range : %.2f, income : %d, cash : %d" % \
			   ( self.speed(), self.range(), self.income(), self.cash() )
