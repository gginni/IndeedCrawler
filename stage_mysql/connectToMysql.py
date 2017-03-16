import MySQLdb
from mongodb.connection import getMongoConnection
from key_words import *
import config

import sys

def getMysqlConnection():
    try:
        db = MySQLdb.connect(host="35.154.170.231", port=3306, user="root", passwd="clim8BTUs", db="zinnov_dev")
    except Exception as e:
        print "could not connect to mysql. %s" %e.message
    return db
    # cursor = db.cursor()
    # return cursor


class ToMysql(object):
    def __init__(self):
        self.conn = getMongoConnection()
        self.mongo_db = self.conn[config.Mongo_DB_NAME]
        self.mysql_db = getMysqlConnection()

    def count_BUs(self, company_name):
        mysql_cities_query = "select distinct city_name from dashboard_sublocations"
        cursor = self.mysql_db.cursor()
        cursor.execute(mysql_cities_query)
        mysql_cities = cursor.fetchall()
        for city in mysql_cities:
            city = city[0]
            for bu in BU_keywords[company_name]:
                count = self.mongo_db[company_name].find({"city": {"$regex": city}, "BU": bu}).count()
		if count != 0:
                    self._insert(city, bu, count, company_name)

    def _insert(self, city, bu, count, company_name):
	company_name = Company[company_name]
        cursor = self.mysql_db.cursor()
        company_id = 'select id from dashboard_companyname where company_name="{0}"'.format(company_name)
        cursor.execute(company_id)
	if cursor.fetchone() == None:
	    print "Company name %s not in database" % company_name
	    sys.exit()
	else:
            company_id = int(cursor.fetchone()[0])

        business_unit_id = "Select id from dashboard_businessunits where business_unit_name='%s' and company_id='%d'" % (bu, company_id)
        cursor.execute(business_unit_id)
	if cursor.fetchone() == None:
	    print "BU name %s not in database" % bu
	    sys.exit()
	else:
            business_unit_id = int(cursor.fetchone()[0])

        sublocation_id = 'select id from dashboard_sublocations where city_name="{0}"'.format(city)
        cursor.execute(sublocation_id)
	if cursor.fetchone() == None:
	    print "City name %s not in database" % city
	    sys.exit()
	else:
            sublocation_id = int(cursor.fetchone()[0])

        query = "INSERT INTO dashboard_bu_jobs(business_unit_id, job_count, sublocation_id) " \
                "values ('%d', '%d', '%d') ON DUPLICATE KEY UPDATE job_count='%d'" % (int(business_unit_id), count, sublocation_id, count)

        cursor = self.mysql_db.cursor()
        try:
            cursor.execute(query)
            self.mysql_db.commit()
        except Exception as e:
            print e.message
            self.mysql_db.rollback()


# i = ToMysql()
# i.count_BUs('Ford Motor Company')
