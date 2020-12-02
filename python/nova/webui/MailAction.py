from nova.api import comm

from Action import Action

class MailAction(Action):
	def actions(self):
		return [ 'sendmail' ]

	def returnToURL(self):
		return 'console.psp'
	
	def sendmail(self):
		if not self.login():
			return
		
		toPlayer = self.request().field('toPlayer')
		subject = 'Communication from Nova player %s' % self._player.name()
		message = self.request().field('message')
		
		successMessage = 'Mail sent to %s' % toPlayer
		
		if self.callMethod(comm.PlayerToPlayerMail().send, successMessage, toPlayer, subject, message):
			self.response().sendRedirect('console.psp?message=%s' % self.urlEncode(successMessage) )

		
