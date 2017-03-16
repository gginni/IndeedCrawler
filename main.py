from mongodb.indeedToMongo import IndeedToMongo
from tagging.tagJobs import TagJobs
from stage_mysql.connectToMysql import ToMysql
import config
import sys, getopt


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hs:t:c:", ["save=", "tag=", "count="])
    except getopt.GetoptError:
        print 'main.py --save "company_name" To save jobs for company' \
              '\nmain.py --tag "company_name" To tag BU again a job \n' \
              '\nmain.py --count "company_name" To count jobs per BU \n'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py --save "company_name" To save jobs for company\n' \
                  'main.py --tag "company_name" To tag BU again a job\n' \
                  'main.py --count "company_name" To count jobs per BU\n'
            sys.exit()
        elif opt in ("-s", "--save"):
            # crawl and save in mongo
            if arg in config.COMPANIES:
                jobs = IndeedToMongo()
                jobs.save_jobs(arg)
            else:
                print "enter correct company name"
        elif opt in ("-t", "--tag"):
            # tag BUs
            if arg in config.COMPANIES:
                jobs = TagJobs()
                jobs.tag_jobs(arg)
            else:
                print "enter correct company name"
        elif opt in ("-c", "--count"):
            # count jobs per BU
            if arg in config.COMPANIES:
                count = ToMysql()
                count.count_BUs(arg)
            else:
                print "enter correct company name"

if __name__ == '__main__':
    main(sys.argv[1:])
