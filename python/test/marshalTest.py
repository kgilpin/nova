from nova.Star import Star
from nova.Player import Player
from nova.util import Log
from nova.xmlrpc.Marshal import Marshal

from xmlrpclib import Marshaller

# Log.enabled = 1

star = Star()
player = Player()
star.setOwner(player)

#print Marshal().findGetMethods( star )
list = Marshal().marshal( star )

#print list
f = open('star.xml', 'w')
f.write( Marshaller().dumps(list) )
f.close()

