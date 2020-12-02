from nova.api import purchase

from Action import Action

class PurchaseAction(Action):
	def actions(self):
		return [ 'purchaseFactories', 'purchaseRange', 'purchaseSpeed', 
				'purchaseProbeShield', 'purchaseNovaShield'  ]

	def returnToURL(self):
		return '/nova/purchase.psp'

	def purchaseFactories(self):
		starName = self.request().field('star')
		numFactories = int(self.request().field('numFactories'))

		message = 'Purchased %d factories on %s' % ( numFactories, starName )

		self.callMethod(purchase.PurchaseFactories().execute, message, starName, numFactories)

	def purchaseRange(self):
		range = float(self.request().field('range'))

		message = 'Purchased %.2f range' % range

		self.callMethod(purchase.PurchaseRange().execute, message, range)

	def purchaseSpeed(self):
		self.login()

		desiredSpeed = float(self.request().field('desiredSpeed'))

		delta = desiredSpeed - self.player().adjustedSpeed()

		message = 'Purchased %.2f speed' % delta

		self.callMethod(purchase.PurchaseSpeed().execute, message, delta / self.game().timeCompression())

	def purchaseProbeShield(self):
		starName = self.request().field('star')

		message = 'Purchased a Probe shield on %s' % starName

		self.callMethod(purchase.PurchaseProbeShield().execute, message, starName)

	def purchaseNovaShield(self):
		starName = self.request().field('star')

		message = 'Purchased a Nova Bomb shield on %s' % starName

		self.callMethod(purchase.PurchaseDeathShield().execute, message, starName)
	
