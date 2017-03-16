from pymongo import MongoClient

def getMongoConnection():
	"""
		This Will make a connection to mongo an returns connection
	"""
	try:
		conn = MongoClient()
	except Exception as e:
		conn = None
		print "Could not connect to MongoDB: %s" % e.message

	return conn