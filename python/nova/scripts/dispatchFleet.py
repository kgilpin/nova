import sys, os
from getopt import getopt

from nova.api import dispatch

def usage(errorMsg=None):
	progName = os.path.basename(sys.argv[0])
	if errorMsg:
		print '%s: error: %s' % (progName, errorMsg)
	print 'Usage: %s -g gameId -u playerName -p password -o origin -d destination -t unitType [ -n numShips ]' % progName
	print
	print '  unitType : Ship, DeathProbe, SpyProbe'
	print '  numShips : default is 1'
	sys.exit(1)

optPairs, files = getopt(sys.argv[1:], 'g:u:p:o:d:t:n:', [])

gameId, playerName, password, origin, destination, unitType, numShips = None, None, '', None, None, None, 1
for key, value in optPairs:
	if key == '-g':
		gameId = int(value)
	elif key == '-u':
		playerName = value
	elif key == '-p':
		password = value
	elif key == '-o':
		origin = value
	elif key == '-d':
		destination = value
	elif key == '-t':
		unitType = value
	elif key == '-n':
		numShips = int(value)

if not gameId or not playerName or not origin or not destination or not unitType:
	usage()

errors = dispatch.Dispatch()._execute(gameId, playerName, password, origin, destination, unitType, numShips)
if len(errors):
	print errors
	sys.exit(1)
sys.exit(0)
