
from NovaPage import NovaPage

from nova.User import User
from nova.engine import store

class LoginAction(NovaPage):
	"""
	A user name and password are provided by the user
	The user may also optionally specify that the login should not expire
	
	The user name and password are checked against the User records in the database
	If successful, userId and password cookies are sent to the browser so that the login
	will be persistent
	"""
	def actions(self):
		return [ 'login' ]
	
	def login(self):
		userName = self.request().fields()['userName']
		password = self.request().fields()['password']
		dontExpire = self.request().field('dontExpireLogin', 0)
		returnToURL = self.request().value('returnToURL')
		
		users = store.get().fetchObjectsOfClass(User, clauses="WHERE name = '%s'" % ( userName) )
		if len(users) == 0 or users[0].password() != password:
			return self.error("Login failed for user '%s'" % userName)
		user = users[0]
			
		optional = {}
		if dontExpire:
			optional['expires'] = 'NEVER'
		
		self.response().setCookie('userId', user.serialNum(), **optional)
		self.response().setCookie('password', password, **optional)
		self.response().sendRedirect(returnToURL)
		
	def error(self, message):
		self.response().sendRedirect('login.psp?error=%s' % self.urlEncode(message))
