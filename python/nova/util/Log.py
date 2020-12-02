
enabled = 0

def log(*args):
	if enabled:
		message = reduce(lambda x, y: "%s%s" % ( x, y ), args)
		print message

def debug(*args):
	log(args)

def warn(*args):
	message = reduce(lambda x, y: "%s%s" % ( x, y ), args)
	print message
