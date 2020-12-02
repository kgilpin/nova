from nova.api.notifications import BattleNotification

from Action import Action

class NotificationsAction(Action):
	def actions(self):
		return [ 'battle' ]

	def returnToURL(self):
		return 'notifications.psp'
	
	def battle(self):
		if not self.login():
			return

		enable = self.request().hasField('enable')
		player = self.player()
		
		if enable:
			self.callMethod(BattleNotification().enable, "Battle notifications enabled")
		else:
			self.callMethod(BattleNotification().disable, "Battle notifications disabled")


		
