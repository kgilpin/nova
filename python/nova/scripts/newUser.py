import sys, os
from getopt import getopt

from nova.engine import store
from nova.User import User

def usage(errorMsg=None):
	progName = os.path.basename(sys.argv[0])
	if errorMsg:
		print '%s: error: %s' % (progName, errorMsg)
	print 'Usage: %s -u userName -p password -e email' % progName
	print
	sys.exit(1)

optPairs, files = getopt(sys.argv[1:], 'n:p:e:', [])

name, password, email = None, None, None
for key, value in optPairs:
	if key == '-u':
		name = value
	elif key == '-p':
		password = value
	elif key == '-e':
		email = value

if not name or not password or not email:
	usage()

store = store.get()
user = User()
user.construct(name, password, email)
store.addObject(user)
store.saveChanges()
