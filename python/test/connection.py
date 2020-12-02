from nova.engine import store

"""
Keeps a shared ObjectStore.

Without a shared instance, each new ObjectStore creates a bunch of connections and eventually
the connection limit of the server is exceeded
"""

def get():
	# Hack in here to discard everything from the previous test
	if store._store is not None:
		store._store.discardEverything()
	return store.get()
