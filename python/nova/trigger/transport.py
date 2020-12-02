import re
from nova.comm import mail

def emailFormat(message):
	"""
	Apply e-mail formatting rules to an event message
	"""
	# Replace '<color>' tags with ''
	# Replace <unit qty=x /> with 'x ships'
	# Replace <unit qty=1 /> with '1 ship'
	# Replace <star name=Orion/> with 'star Orion'
	eventMessageReplacements = [ ( r'<color>', ''),
								 ( r'<br/>', '\n'),
								 ( r'</color>', '' ),
								 ( r'<unit qty=1\s*/>', r'1 ship'),
								 ( r'<unit qty=(\d+)\s*/>', r'\1 ships' ),
								 ( r'<star name=([^/]+)/>', r'star \1' ) ]

	for pattern, repl in eventMessageReplacements:
		message = re.sub(pattern, repl, message)
	return message

class Transport:
	def sendMessage(self, player, message):
		"""
		Send a Message
		"""
		raise NotImplementedError, self.__class__
		

class EmailTransport(Transport):
	"""
	Sends a Message via e-mail
	"""
	
	def sendMessage(self, player, message):
		mailMessage = mail.SystemToPlayerMessage(mail.smtp())
		mailMessage.send(player, emailFormat(message.subject()), emailFormat(message.body()))
	
class DummyTransport(Transport):
	"""
	Saves the player and message in eponymous variables
	"""
	def __init__(self):
		self.messages = []

	def clear(self):
		self.messages = []
		
	def sendMessage(self, player, message):
		self.messages.append( ( player, message ) )

	def __repr__(self):
		return str(self.messages)
		