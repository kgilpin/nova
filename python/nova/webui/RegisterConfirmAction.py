from nova.api import user

from WebKit.Page import Page

class RegisterConfirmAction(Page):
	def respondToGet(self, transaction):
		self.response().sendRedirect("/nova/registerConfirm.psp")
