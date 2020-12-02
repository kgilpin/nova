import method

from nova.comm import mail
from nova.Player import Player

class PlayerToPlayerMail(method.APIMethod):
	def send(self, gameId, playerName, password, toPlayerName, subject, message):
		"""
		Sends e-mail from one player to another
		Returns an empty error map if the message is sent successfully
		Otherwise, returns the error message with the key 'mail'
		"""
		game = self.game(gameId)
		fromPlayer = self.login(game, playerName, password)
		toPlayer = self.findObject(Player, "WHERE gameId = %s AND name = '%s'" % ( game.sqlObjRef(), toPlayerName ), 
			"Can't find player %s" % toPlayerName)
		smtp = mail.smtp()
		try:
			sender = mail.PlayerToPlayerMessage(smtp)
			if sender.send(fromPlayer, toPlayer, subject, message):
				return {}
			else:
				return { 'mail' : 'Unable to send message to %s' % toPlayerName }
		finally:
			smtp.quit()
		
		
