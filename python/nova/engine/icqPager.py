
class Page:
	def __init__(self, uin, event):
		"""
		Construct an ICQ Page with the user ID number and the Event whose
		message will be sent		
		"""
		self._uin = uin
		self._event = event

	def send(self):
		pass
