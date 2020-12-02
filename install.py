import sys, os
from getopt import getopt

sys.path.insert(1, 'python')

dbUser = None
dbPassword = ''
url = 'http://localhost/cgi-bin/OneShot.cgi/Nova'
smtp = 'localhost'

def usage(errorMsg=None):
	progName = os.path.basename(sys.argv[0])
	if errorMsg:
		print '%s: error: %s' % (progName, errorMsg)
	print 'Usage: %s -u dbUser [ -p dbPassword ] [ -s SMTP] [ --url novaURL ]' % progName
	print
	print '  novaURL : default is %s' % url
	print '  SMTP    : SMTP host. Default is localhost'
	sys.exit(1)

dbTemplate = """
{
	'DBUser' : '%s',
	'DBPassword' : '%s'
}
"""

testTemplate = """
{
	'NovaURL' : '%s',
}
"""

commTemplate = """
{
	'SMTPHost' : '%s',
}
"""

optPairs, files = getopt(sys.argv[1:], 'u:p:s:', [ 'url=' ])

if len(optPairs) < 1:
	usage('Missing options.')

for key, value in optPairs:
	if key == '-p':
		dbPassword = value
	elif key == '-u':
		dbUser = value
	elif key == '-s':
		smtp = value
	elif key == '--url':
		url = value

if not dbUser:
	usage()

file = open('python/nova/engine/DB.config', 'w')
file.write(dbTemplate % ( dbUser, dbPassword ))
# Restrict permissions?
# os.chmod(configFile, '600')
file.close()

file = open('python/test/Test.config', 'w')
file.write(testTemplate % ( url ))
file.close()

file = open('python/nova/comm/Comm.config', 'w')
file.write(commTemplate % ( smtp ))
file.close()

from nova.engine import store, newGame, mapLoader
from nova.TriggerDefinition import installDefaultTriggers
from nova.User import User
from mx import DateTime

db = store.get()

def createUser(name, password, email):
	users = db.fetchObjectsOfClass(User, clauses="WHERE name = '%s'" % name)
	if not len(users):
		user = User()
		user.construct(name, password, email)
		db.addObject(user)
	else:
		user = users[0]
	return user

users = [ createUser('kevin', 'kevin', 'kgilpin@yahoo.com'),
			 createUser('scott', 'scott', 'scott@westslopesoftware.com'),
			 createUser('dave', 'dave', 'daved@alum.mit.edu') ]

installDefaultTriggers(db)			 
			 
db.saveChanges()

loader = mapLoader.ImageMapLoader('maps/scatter.bmp')
map = loader.loadStarMap()
# Create a new game which stars now and lasts for 1 hour, running at 500x speed
ng = newGame.NewGame(map, users, DateTime.now(), DateTime.DateTimeDelta(0, 1), db, timeCompression=500)

print 'Created game %d' % ng.game().serialNum()
