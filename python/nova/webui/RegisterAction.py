from nova.api import user

from Action import Action

class RegisterAction(Action):
	def actions(self):
		return [ 'register'  ]

	def forwardToURL(self):
		return "/nova/registerSubmitted.psp"

	def returnToURL(self):
		return '/nova/register.psp'

	def register(self):
		userName = self.request().field('userName')
		password = self.request().field('password')
		email = self.request().field('email')

		message = 'Registered new user %s' % userName

		self.callMethodRaw(user.Register().execute, message, userName, password, email)
