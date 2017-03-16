########### Python 2.7 #############
import urllib
import requests, json
import lxml.html
from microsofttranslator import Translator
from langdetect import detect
from mongodb import connection
Mongo_DB_NAME = 'Indeed'
COMPANY = ['Continental', 'Ford Motor Company']
KEY = '6437595457989494'
countries = ['us', 'ar']

translator = Translator('zinnovIndeed', 'zinnovJobClassification')

class IndeedCrawl(object):

    def __init__(self, company_name, key):
        self.query = "company:({0})".format(company_name)
        self.endpoint = 'http://api.indeed.com/ads/apisearch'
        self.key = key
        self.conn = connection.getMongoConnection()
        self.db = self.conn[Mongo_DB_NAME]

    def _create_params(self, query, key, start, country, count=10):
        params = urllib.urlencode({
            # Request parameters
            'publisher': key,
            'q': query,
            'limit': count,
            'co': country,
            'start': start,
            'sort': 'date',
            'st': 'employer',
            'format': 'json',
            'v': 2,
        })
        return params

    def search(self, start, country, count):
        jobs = []
        try:
            while count > start:
                params = self._create_params(self.query, self.key, start, country, count)
                response = requests.get(self.endpoint, params)
                response = json.loads(response.text)
                #print "got it %s" % response
                count = response['totalResults']
                for res in response['results']:
                    print count
                    if count == 0:
                        break
                    if res.get('url'):
                        url = res.get('url')
                        res2 = requests.get(url)
                        jd = ""
                        summary = lxml.html.fromstring(res2.text)
                        for span in summary.xpath('//span[@id="job_summary"]'):
                            for x in span.itertext():
                                job_sum = x.encode('utf-8')
                                # check if some other opensource
                                # detection
                                #lan = detect(job_sum)
                                #print str(lan)
                                #if str(lan) != 'en':
                                #    print "use translator"
                                    #job_sum = translator.translate(job_sum, "en")
                                jd += job_sum
                        res['job_summary'] = jd
                        print res
                        jobs.append(res)
                start += 25
            return jobs
        except Exception as e:
            print e.message

####################################