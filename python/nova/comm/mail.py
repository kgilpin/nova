from smtplib import SMTP
import os
import log4py

from MiddleKit.Run.MySQLObjectStore import MySQLObjectStore
from MiscUtils.Configurable import Configurable

Log = None

# Can use cc: to send a carbon copy
# See http://www.faqs.org/rfcs/rfc822.html
messageTemplate = 'From: %s\r\nTo: %s\r\nSubject:%s\r\n%s'


class CommConfig(Configurable):
	def smtpHost(self):
		return self.setting('SMTPHost')

	def systemAddress(self):
		return self.setting('SystemAddress')

	def defaultConfig(self):
		return { 'SMTPHost' : 'localhost', 'SystemAddress' : '"Nova" <nova@ironworks.cc>' }

	def configFilename(self):
		dir = os.path.dirname(__file__)
		return os.path.join(os.path.abspath(dir), 'Comm.config')
		
def smtp():
	"""
	Returns a new connected SMTP object
	Use the quit() method when you are done with it
	"""
	config = CommConfig()
	smtp = SMTP()
	# smtp.set_debuglevel(1)
	# Add authentication here if you ever need to
	smtp.connect(config.smtpHost())
	return smtp	

class Message:
	def __init__(self, smtp):
		self._smtp = smtp

	def send(self, fromAddr, toAddr, subject, msg):
		"""
		Returns 1 if the message is successfully sent
		"""
		msg = messageTemplate % ( fromAddr, toAddr, subject, msg )
		try:
			self._smtp.sendmail(fromAddr, toAddr, msg)
			return 1
		except Exception, x:
			import traceback
			traceback.print_exc()
			Log.error( 'Error sending message %s: %s' % ( msg, x ))
			return 0
			
	def playerToAddress(self, player):
		return '"%s" <%s>' % ( player.name(), player.user().email() )		

	def userToAddress(self, user):
		return '"%s" <%s>' % ( user.name(), user.email() )		

class PlayerToPlayerMessage(Message):
	def send(self, fromPlayer, toPlayer, subject, msg):
		fromAddr = self.playerToAddress(fromPlayer)
		toAddr = self.playerToAddress(toPlayer)
		return Message.send(self, fromAddr, toAddr, subject, msg)		

class SystemToPlayerMessage(Message):		
	def send(self, toPlayer, subject, msg):
		config = CommConfig()
		fromAddr = config.systemAddress()
		toAddr = self.playerToAddress(toPlayer)
		return Message.send(self, fromAddr, toAddr, subject, msg)		

class SystemToUserMessage(Message):		
	def send(self, toUser, subject, msg):
		config = CommConfig()
		fromAddr = config.systemAddress()
		toAddr = self.userToAddress(toUser)
		return Message.send(self, fromAddr, toAddr, subject, msg)		
		
Log = log4py.Logger().get_instance(Message)		
