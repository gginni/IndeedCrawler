########### Python 2.7 #############
import urllib
import requests, json
import lxml.html

class IndeedCrawl(object):

    def __init__(self, company_name, key):
        self.query = "company:({0})".format(company_name)
        self.endpoint = 'http://api.indeed.com/ads/apisearch'
        self.key = key

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
                count = response['totalResults']
                print count
                for res in response['results']:
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
                                jd += job_sum
                        res['job_summary'] = jd
                    print res
                    jobs.append(res)
                start += 25
            return jobs
        except Exception as e:
            print e.message

####################################
