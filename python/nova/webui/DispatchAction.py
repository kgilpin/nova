from nova.api import dispatch

from Action import Action

class DispatchAction(Action):
	def actions(self):
		return [ 'ships', 'spy', 'bomb' ]

	def returnToURL(self):
		return self.request().field('returnToURL')
	
	def ships(self):
		numShips = self.request().field('numShips')
		if numShips == '': numShips = 0
		numShips = int(numShips)

		message = 'Sending <unit qty=%d /> from %s to %s' % ( numShips, self._origin(), self._destination() )
		
		command = dispatch.DispatchFleet()
		self._delay(command)
		
		self.callMethod(command.execute, message, self._origin(), self._destination(), numShips)

	def spy(self):

		message = 'Sending a probe from %s to %s' % ( self._origin(), self._destination() )

		command = dispatch.DispatchSpyProbe()
		self._delay(command)
		
		self.callMethod(command.execute, message, self._origin(), self._destination())

	def bomb(self):
		message = 'Sending a WID (Weapon of Inappropriate Destruction) from %s to %s' % ( self._origin(), self._destination() )
		
		command = dispatch.DispatchDeathProbe()
		self._delay(command)
		
		self.callMethod(command.execute, message, self._origin(), self._destination())

	def _delay(self, dispatch):
		delay = self.request().field('delay', 0)
		if delay == '': delay = 0
		delay = int(delay)
		if delay < 0:
			delay = 0
		dispatch.setDelayMinutes(delay)		

	def _origin(self):
		return self.request().field('origin')

	def _destination(self):
		return self.request().field('destination')
		
