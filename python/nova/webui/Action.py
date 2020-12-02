import types

import log4py

from GamePage import GamePage

class Action(GamePage):
	def returnToURL(self):
		"""
		Each action is posted from a particular page. This method should get the base URL that the
		client will be sent back to after the action is complete
		"""
		raise NotImplementedError, self.__class__

	def forwardToURL(self):
		"""
		Optional URL to which the action will forward after successful invocation
		"""
		return None

	def callMethod(self, method, message, *params):
		"""
		Invokes the API 'method' with the parameter set [ *self.credentials(), params ]
		The user is then redirected to self.returnToURL, with either the success 'message',
		or a failure message returned by the method.
		"""
		self.login()
		args = self._credentials()
		args.extend(params)
		return self.callMethodRaw(method, message, *args)

	def callMethodRaw(self, method, message, *args):
		"""
		Invokes the API 'method' with the parameter set [ args ]
		The user is then redirected to self.returnToURL, with either the success 'message',
		or a failure message returned by the method.
		"""
		try:
			errors = method(*args)
			if not isinstance(errors, types.DictType) or not len(errors):
				url = self.forwardToURL()
				if url is None:
					url = self.returnToURL()
				self.response().sendRedirect('%s?message=%s' % ( url, self.urlEncode(message) ) )
				return 1
			else:
				Log.warn(errors)				
				self.response().sendRedirect('%s?error=%s' % ( self.returnToURL(), self.urlEncode(errors.values()[0])) )
		except Exception, x:
			Log.warn(x)
			self.response().sendRedirect('%s?error=%s' % ( self.returnToURL(), self.urlEncode(str(x))) )
		return 0
			
Log = log4py.Logger().get_instance(Action)


