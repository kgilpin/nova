from WebKit.Page import Page

class index(Page):
	def writeContent(self):
		self.writeln('<p>Space Empires Lives!</p>')
