# -*- coding: utf-8 -*-
from langdetect import detect
from mongodb.connection import getMongoConnection
import config
import sys
from mstranslator import Translator
translator = Translator('a4462ffdf09e4ce08bb2df759478229a')

def translate(company_name):
    conn = getMongoConnection()
    db = conn[config.Mongo_DB_NAME]
    while db[company_name].find({"translated": "false"}).count() > 0:
        job = db[company_name].find_one({"translated": "false"})
        try:
            lan = detect(unicode(job['job_summary'], "utf-8"))
        except:
            lan = detect(job['job_summary'])
        print lan
        print job
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
                        job[key] = job[key].encode("ascii", "ignore")
                        job[key] = translator.translate(job[key], lang_to="en")
                        flag = 1
                    else:
                        print "couldn't translate %s" % job['url']
                    print flag
                    if flag == 1:
                        db[company_name].update({"url": job["url"]},
                                                {"$set": {"job_summary": job[key]}}, upsert=False, multi=False)
        db[company_name].update({"url": job["url"]},
                                {"$set": {"translated": "true"}}, upsert=False, multi=False)

if __name__ == '__main__':
    company_name = sys.argv[1]
    translate(company_name)
    # companies = ['Google', 'Microsoft']
    # #companies = ['Bosch', 'Valeo', 'Continental']
    # companies = ['Ford Motor Company']
    # for company in companies:
    #     translate(company)
