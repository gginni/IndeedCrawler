from mongodb import connection
from indeed.indeed_crawl import IndeedCrawl
import csv
import config
from pymongo.errors import DuplicateKeyError

class IndeedToMongo(object):
    def __init__(self):
        self.conn = connection.getMongoConnection()
        self.db = self.conn[config.Mongo_DB_NAME]

    def save_jobs(self, company_name):
	# no need to remove documents
	# as duplicate key constraint is added
        # self.db[company_name].remove({})
        indeed_jobs = IndeedCrawl(company_name, config.KEY)
        with open('countries_new.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                print "country %s" % row[0]
                country = str(row[0])
                start = 1
                jobs = indeed_jobs.search(start, country, 1000)
                if jobs:
                    for job in jobs:
			try: 
	                        self.db[company_name].insert(job)
        	                self.db[company_name].update({},
                	                                    {"$set": {"BU": ""}}, upsert=False, multi=False)
				self.db[company_name].update({},
                                                            {"$set": {"translated": "false"}}, upsert=False, multi=False)
			except DuplicateKeyError as e:
				print "jobKey already exists %s" % e.message
			except Exception as e:
				print e.message

# jobs = IndeedToMongo()
# jobs.save_jobs('Ford Motor Company')
# jobs.save_jobs('Continental')
