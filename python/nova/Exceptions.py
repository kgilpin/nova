
class InvalidEventException(Exception):
	"""
	Thrown by an event when it cannot be successfully executed. For instance, if
	the event requires more wealth than the player has.
	"""
	pass
	
