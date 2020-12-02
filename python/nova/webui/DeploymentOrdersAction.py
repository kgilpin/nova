from nova.api import deploy
from nova.engine import find

from MiscUtils import NoDefault

from Action import Action

class DeploymentOrdersAction(Action):
	def actions(self):
		return [ 'orders' ]

	def returnToURL(self):
		return "deployment.psp"
		
	def orders(self):
		"""
		Form input is received with data for each orgin star.
		For each star, a <select> input with name 'destination%d' % origin.serialNum()
			is received, along with a text input with name 'garrison%d' % origin.serialNum()
		For each star, this method should update the AutoDeployTrigger for that star to make sure
			it reflects the user's selections
		"""
		if not self.login():
			return
			
		player = self.player()

		method = deploy.DeploymentOrders()

		# Find all the stars which used to have a deployment order but no longer do, and cancel
		#   each of them
		existingOrders = find.getDeploymentOrders(player)
		for origin in existingOrders.keys():
			if self.starField('destination', origin, 'None') == 'None':
				args = self._credentials()
				args.append(origin.serialNum())
				method.undeploy(*args)

		stars = find.getOwnedLiveStars(player)
		for origin in stars:
			if self.starField('destination', origin, 'None') != 'None':
				destinationId = long(self.starField('destination', origin))
				garrison = self.starField('garrison', origin, 0)
				if garrison != '':
					garrison = int(garrison)
				else:
					garrison = 0
				args = self._credentials()
				args.extend([ origin.serialNum(), destinationId, garrison ])
				method.deploy(*args)
		self.response().sendRedirect(self.returnToURL())
					
	def starField(self, fieldName, star, default=NoDefault):
		return self.request().field('%s%d' % ( fieldName, star.serialNum() ), default)				
		