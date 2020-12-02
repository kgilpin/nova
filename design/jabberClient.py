import sys

import jabber

DEBUG_LEVEL = 1
INFO_LEVEL = 2

def messageCB(con, msg):
	"""Called when a message is recieved"""
	if msg.getBody(): ## Dont show blank messages ##
		print '<' + str(msg.getFrom()) + '>' + ' ' + msg.getBody()
		
# should make debug level settable in config
con = jabber.Client(host='jabber.org', debug=INFO_LEVEL, log=sys.stderr)
con.setMessageHandler(messageCB)

try:
	con.connect()
except IOError, e:
	print "Couldn't connect: %s" % e
	sys.exit(1)
else:
	print "Connected"

server = 'jabber.org'
username = 'kgilpin'
password = '5mang'
resource = 'kchat'

if con.auth(username, password, resource):
	print "Logged in as %s to server %s" % (username, server)
else:
	print "eek -> ", con.lastErr, con.lastErrCode

JID = username + '@' + server + '/' + resource
print "JID", JID
JID = JID

msg = jabber.Message('kgilpin', 'Hello Kevin')
msg.setType('chat')
print "<%s> %s" % (JID, msg.getBody())
con.send(msg)

con.disconnect()
print "Bye!"
