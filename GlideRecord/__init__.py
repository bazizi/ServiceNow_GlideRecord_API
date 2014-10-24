"""
    Author: Behnam Azizi
            cgi.sfu.ca/~bazizi

    Date: Oct. 11, 2014

    Description: ServiceNow Rest API (GlideRecord) for Python
                 Based on ServiceNow GlideRecord documentation: 
                   http://wiki.servicenow.com/index.php?title=GlideRecord

"""

import urllib2
import base64
import json
import re
import getpass
import sys

class GlideRecord:
    def __init__(self, tableName):
        self.query_data = dict()
        self.username = None
        self.password = None

        self.encodedAuth = None
        self.query_data['server'] = None
        self.query_data['tableName'] = tableName
        self.query_data['actionType'] = "getRecords"
        self.results = {}
        self.currentIndex = -1
        self.query_data['rowCount'] = 100
        self.query_data['sysparm_query'] = None


    def set_server(self, srvname):
        self.query_data['server'] = srvname
        self.query_data['URL'] = '%s/%s.do?JSONv2&sysparm_record_count=%s&sysparm_action=%s&sysparm_query=' % (self.query_data['server'], self.query_data['tableName'], self.query_data['rowCount'], self.query_data['actionType'])
        #print self.query_data['URL']

    def set_credentials(self, uname, passwd):
        self.username = uname
        self.password = passwd
        self.reset_credentials()


    def get_credentials(self):
            self.username = raw_input("Please enter ServiceNow username: ")
            self.password = getpass.getpass("Please enter ServiceNow password for %s:" % self.username)
            self.reset_credentials()


    def reset_credentials(self):
        self.encodedAuth = base64.b64encode(self.username + ":" + self.password)

    def is_user_creds_valid(self):
        request = re.sub('sysparm_record_count=[^&]+', 'sysparm_record_count=1', self.query_data['URL'])
        result = self.get_url(request)
        if result:
            return True
        return False


    def get(self, key, value):
        self.addQuery(key, value)
        self.setRowCount(1)
        self.query()
        if self.getRowCount() == 1:
            return True
        return False

    def hasNext(self):
        if self.getRowCount() > 0 and self.currentIndex + 1 < self.getRowCount():
            self.currentIndex += 1
            return True
        return False

    def addEncodedQuery(self, queryString):
        if not self.query_data['sysparm_query']:
            self.query_data['sysparm_query'] = queryString
        else:
            self.query_data['sysparm_query'] += "^" + queryString
        #print self.query_data

    def getValue(self, key):
        rs = self.results[self.currentIndex][key]
        return rs

    def setValues(self, key, value):
        self.results[self.currentIndex][key] = value
        self.refreshQuery()
        self.post_url(request, json.dumps({key:value}))
        self.query()

    def insert(self, data):
        request = re.sub('sysparm_action=[^&]+', 'sysparm_action=%s' % 'insert', self.query_data['URL'])
        self.post_url(request, json.dumps(data))

    def delete(self):
        query = self.query_data['sysparm_query']
        if not re.findall('syparm_sys_id', query):
            print("ERROR: Could not delete the record. 'sysparm_sys_id' is not specified")
        url = self.query_data['URL']
        request = re.sub('sysparm_action=[^&]+', 'sysparm_action=%s' % 'deleteRecord', url)
        data = json.dumps({
            'sysparm_query' : self.query_data['sysparm_query']
        })
        #print data
        self.post_url(request, data)

    def deleteMultiple(self):
        url = self.query_data['URL']
        request = re.sub('sysparm_action=[^&]+', 'sysparm_action=%s' % 'deleteMultiple', url)
        self.post_url(request, json.dumps({
            'sysparm_query' : self.query_data['sysparm_query']
        }))


    def refreshQuery(self):
        self.query_data['URL'] = re.sub('sysparm_action=[^&]+', 'sysparm_action=%s' % self.query_data['actionType'], self.query_data['URL'])
        self.query_data['URL'] = re.sub('sysparm_record_count=[^&]+', 'sysparm_record_count=%s' % self.query_data['rowCount'], self.query_data['URL'])

    def getRow(self):
        rs = []
        for value in self.results[self.currentIndex].values():
            rs.append(str(value))
        return rs


    def getHeaders(self):
        rs = []
        for key in self.results[self.currentIndex].keys():
            rs.append(str(key))
        return rs

    def next(self):
        if self.currentIndex + 1 < self.getRowCount():
            self.currentIndex += 1
            return  True
        return  False

    def addQuery(self, key, value=""):
        if not self.query_data['sysparm_query']:
            self.query_data['sysparm_query'] = "%s=%s" % (key, value)
        else:
            self.query_data['sysparm_query'] += "^%s=%s" % (key, value)

        #print self.query_data

    def query(self):
        request = self.query_data['URL'] + self.query_data['sysparm_query']
        raw_json = self.get_url(request)
        #print raw_json.read()
        if raw_json:
            self.results = json.load(raw_json)['records']

    def getQuery(self):
        return self.query_data['URL']

    def setRowCount(self, n):
        self.query_data['rowCount'] = n
        self.refreshQuery()

    def getRowCount(self):
        return len(self.results)

    #This is a helper function that is used to send GET, PUT or POST requests to Jira
    #This function is used by other functions and not the user directly
    def req_data(self, url, data, method):
        """Sends a request for data"""
        values = data
        #print "Requesting: %s" % url
        if data != '':
            #print "Using Data: %s" % data
            req = urllib2.Request(url, data=values)

        else:
            req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Basic %s' % self.encodedAuth)
        req.get_method = lambda: method

        try:
            resp = urllib2.urlopen(req)

            #print resp.read()
            return resp
        except urllib2.HTTPError, error:
            error = error.read()
            print("\n*** Sorry, the provided ServiceNow Username/Password was wrong or "
                  "this user (%s) is Unauthorized to send REST requests ***" % self.username)
            print("\n*** If username and password are correct, there is a chance this account is "
                  "blocked due to many unsuccessful login attempts ***")
            sys.exit(0)

            #print(error)

    #This function sends GET requests to a given URI
    def get_url(self, url):
        """Used for sending/receiving GET requests to a URL"""
        return self.req_data(url, '', 'GET')

    #This function sends PUT requests to a given URI
    def put_url(self, url, data):
        """Used for sending/receiving PUT requests to a URL"""
        return self.req_data(url, data, 'PUT')

    #This function sends POST requests to a given URI
    def post_url(self, url, data):
        """ Used for sending/receiving POST requests to a URL"""
        return self.req_data(url, data, 'POST')
