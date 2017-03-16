from langdetect import detect
from mongodb.connection import getMongoConnection
import config
import sys
from mstranslator import Translator
translator = Translator('c64707b4ecb74bd7b4a78ead5fa7b708')

def translate(company_name):
    conn = getMongoConnection()
    db = conn[config.Mongo_DB_NAME]
    print db
    print "something yar"
    while db[company_name].find({"translated": True}).count() > 0:
        job = db[company_name].find_one({"translated": True})
        lan = detect(job['snippet'])
        if str(lan) != 'en':
            for key in job:
                if key == "city" or key == "snippet":
                    job[key] = translator.translate(job[key], lang_to="en")
                    db[company_name].update({"url": job["url"]},
                                            {"$set": {key: job[key]}}, upsert=False, multi=False)
                if key == "job_summary":
                    flag = 0
                    try:
                        job[key] = translator.translate(unicode(job[key], "utf-8"), lang_to="en")
                        flag = 1
                    except:
                        job[key] = translator.translate(job[key], lang_to="en")
                        flag = 1
                    else:
                        print "couldn't translate %s" % job['url']
                    print flag
                    if flag == 1:
                        db[company_name].update({"url": job["url"]},
                                                {"$set": {"job_summary": job[key]}}, upsert=False, multi=False)
        db[company_name].update({"url": job["url"]},
                                {"$set": {"translated": False}}, upsert=False, multi=False)

if __name__ == '__main__':
    company_name = sys.argv[1]
    translate(company_name)