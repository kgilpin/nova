from nova.api import dispatch

from Action import Action

class AbortAction(Action):
	def actions(self):
		return [ 'abort' ]

	def returnToURL(self):
		return 'console.psp'
	
	def abort(self):
		departureId = int(self.request().field('departureId'))

		message = 'Orders canceled'
		
		abort = dispatch.Abort()
		self.callMethod(abort.execute, message, departureId)

		
