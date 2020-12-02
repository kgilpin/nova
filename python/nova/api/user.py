import random

import method

from nova.comm import mail
from nova.engine import store
from nova.User import User

msg = """
Welcome to Nova!

To confirm your membership, please visit the followming URL:
	
http://ironworks.cc/nova/RegisterConfirmAction.py?key=%s

Thank you.
"""

class Register(method.APIMethod):
	def execute(self, userName, password, email):
		existingUsers = store.get().fetchObjectsOfClass(User, "WHERE name = '%s'" % userName)
		if len(existingUsers):
			return { userName : "User name '%s' is already taken" % userName}
		existingUsers = store.get().fetchObjectsOfClass(User, "WHERE email = '%s'" % email)
		if len(existingUsers):
			return { userName : "Email address '%s' is already in use. Perhaps you have already registered?" % email}
		user = User()
		user.construct(userName, password, email)
		store.get().addObject(user)
		key = random.randint(0, 1e6)
		mail.SystemToUserMessage(mail.smtp()).send(user, "Welcome to Nova!", msg % key)
		store.get().saveChanges()
		# No news is good news
	