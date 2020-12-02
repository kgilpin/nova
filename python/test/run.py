import sys, os, unittest
from getopt import getopt

sys.path.insert(0, '.')

from nova.api import dispatch

def usage(errorMsg=None):
	progName = os.path.basename(sys.argv[0])
	if errorMsg:
		print '%s: error: %s' % (progName, errorMsg)
	print 'Usage: %s -t <tests>' % progName
	print
	print '  tests : comma-separated list of test file names'
	sys.exit(1)

optPairs, files = getopt(sys.argv[1:], 't:', [])

names = []
for key, value in optPairs:
	if key == '-t':
		names = value.split(',')

basedir = os.path.abspath('.').replace('\\', '/')
if not basedir.endswith('/'):
	basedir = '%s/' % basedir

print 'Working directory : %s ' % basedir
		
tests = []
for name in names:
	if name.endswith('.py'):
		name = name[0:-3]
	if name.lower().startswith(basedir.lower()):
		name = name[len(basedir):]
	name = name.strip().replace('/', '.')
	tests.append(name)

print 'Running tests : %s' % ', '.join(tests)

loader = unittest.TestLoader()
suite = loader.loadTestsFromNames( tests )
testRunner = unittest.TextTestRunner()
result = testRunner.run(suite)
sys.exit(not result.wasSuccessful())

#for test in tests:
#	print 'Running %s' % test
#	p = unittest.TestProgram(argv=sys.argv[0:1],module=None,defaultTest=test)
