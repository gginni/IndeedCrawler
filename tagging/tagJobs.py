from mongodb import connection
from key_words import *
import config

class TagJobs(object):
    def __init__(self):
        pass

    def tag_jobs(self, company_name):
        mongo = connection.getMongoConnection()
        db = mongo[config.Mongo_DB_NAME]
        while db[company_name].find({"BU": ""}).count() > 0:
            job = db[company_name].find_one({"BU": ""})

            if self.to_ignore(job['jobtitle']):
                db[company_name].update({"url": job['url']},
                                        {"$set": {"BU": "invalid"}}, upsert=False, multi=False)
            else:
                bu = self.calculate_tag(company_name, job["job_summary"])
                db[company_name].update({"url": job['url']},
                                        {"$set": {"BU": bu}}, upsert=False, multi=False)

    def to_ignore(self,title):
        title = title.encode("utf-8")
        title = title.lower()
        for word in IGNORE:
            if title.count(word.lower()) > 0:
                return True
        return False

    def calculate_tag(self, company_name, summary):
        summary = summary.encode("utf-8")
        summary = summary.lower()
        count = {}
        for bu in BU_keywords[company_name]:
            count[bu] = 0
        for bu, key_word in BU_keywords[company_name].iteritems():
            for word in key_word:
                key_count = summary.count(word.lower())
                count[bu] += key_count

        if all(value == 0 for value in count.values()):
            return "NA"
        else:
            maxi = max(count, key=count.get)
            maxi_value = count[maxi]
            maximum_count = []
            for bu, v in count.iteritems():
                if maxi_value == v:
                        maximum_count.append(bu)
            if len(maximum_count) > 1:
                return maximum_count
            else:
                return maximum_count[0]


# jobs = TagJobs()
# #jobs.tag_jobs('Ford Motor Company')
# jobs.tag_jobs('Ford Motor Company')
