import os, sys

from nova.webui import format

from nova.engine import store
from WebKit.Page import Page

class NovaPage(Page):
	def store(self):
		return store.get()

	def formatEventMessage(self, message):
		"""
		Formats the markup that is returned in the event message strings. See nova.Event#uiDescription
		"""
		return format.formatEventMessage(message)

	def login(self, returnToURL):
		"""
		Return true if the user is logged in. This is determined by looking at browser cookies.
		"""
		if not self.request().hasValue('userId') or \
			not self.request().hasValue('password'):
			self.response().sendRedirect('/nova/login.psp?returnToURL=%s' % returnToURL)
			return 0
		return 1

	def mapDir(self):
		dir = os.path.dirname(__file__)
		return os.path.join(os.path.abspath(dir), 'maps')
	

