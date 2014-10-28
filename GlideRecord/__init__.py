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
import  time

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

    #Sets the URL to the servicenow server for future queries (e.g., ubc.service-now.com)
    def set_server(self, srvname):
        self.query_data['server'] = srvname
        self.query_data['URL'] = '%s/%s.do?JSONv2&sysparm_record_count=%s&sysparm_action=%s&sysparm_query=' % (self.query_data['server'], self.query_data['tableName'], self.query_data['rowCount'], self.query_data['actionType'])
        #print self.query_data['URL']

    #Sets the user credentials (username and password) for future queries
    def set_credentials(self, uname, passwd):
        self.username = uname
        self.password = passwd
        self.reset_credentials()

    #Running this function makes the script ask for username and password
    #password is entered in hidden format
    #this function is used instead of the above function,
    # in case users do not want to provide their credentials in plain text
    def get_credentials(self):
            self.username = raw_input("Please enter ServiceNow username: ")
            self.password = getpass.getpass("Please enter ServiceNow password for %s:" % self.username)
            self.reset_credentials()

    #This is a helper function, not to be used directly
    #It basically stored the username and password in encrypted format, for future queries
    def reset_credentials(self):
        self.encodedAuth = base64.b64encode(self.username + ":" + self.password)

    #This function is not used, please ignore this
    def is_user_creds_valid(self):
        request = re.sub('sysparm_record_count=[^&]*', 'sysparm_record_count=1', self.query_data['URL'])
        result = self.get_url(request)
        if result:
            return True
        return False

    #It checks if there is a record in the table which has key==value, returns a boolean
    def get(self, key, value):
        self.addQuery(key, value)
        self.setRowCount(1)
        self.query()
        if self.getRowCount() == 1:
            return True
        return False

    #If the cursor is not at the end of the records returns True
    #Else returns false
    def hasNext(self):
        if self.getRowCount() > 0 and self.currentIndex + 1 < self.getRowCount():
            self.currentIndex += 1
            return True
        return False

    #Adds an encoded query to the query string (e.g., "u_phone_number=12345")
    def addEncodedQuery(self, queryString):
        if not self.query_data['sysparm_query']:
            self.query_data['sysparm_query'] = queryString
        else:
            self.query_data['sysparm_query'] += "^" + queryString
        #print self.query_data

    #Gets the value of the key column in the row where the cursor is pointing to
    #For example, getValue("u_phone_number")
    def getValue(self, key):
        rs = self.results[self.currentIndex][key]
        return rs

    #Sets the value of <key> in all records returned by the query
    #for example, setValues("u_phone_number", "12345") sets values of all phone numbers to '12345'
    def setValues(self, key, value, show_results=True):
        request = re.sub('sysparm_action=[^&]*', 'sysparm_action=%s' % 'update', self.query_data['URL'])
        request +=  self.query_data['sysparm_query']
        req_data = json.dumps({key:value})
        rs = self.post_url(request, req_data)
        self.query()
        for i in range(len(self.results)):
            self.results[i][key] = value
        #print json.load(rs)
        if show_results:
            updated_records = json.load(rs)['records']
            print "Number of updated records: " + str(len(updated_records))
            print "The following records were updated:"
            for r in updated_records:
                print r['number']

    #Inserts a new ticket into servicenow based on the JSON-fromatted data
    def insert(self, data):
        request = re.sub('sysparm_action=[^&]*', 'sysparm_action=%s' % 'insert', self.query_data['URL'])
        self.post_url(request, json.dumps(data))

    #If 'sysparm_sys_id' is already added to the query string,
    #then this function deletes the record with the given 'sysparm_sys_id'
    def delete(self):
        query = self.query_data['sysparm_query']
        if not re.findall('syparm_sys_id', query):
            print("ERROR: Could not delete the record. 'sysparm_sys_id' is not specified")
            sys.exit(0)
        url = self.query_data['URL']
        request = re.sub('sysparm_action=[^&]*', 'sysparm_action=%s' % 'deleteRecord', url)
        data = json.dumps({
            'sysparm_query' : self.query_data['sysparm_query']
        })
        #print data
        self.post_url(request, data)

    #Deletes ALL records from servicenow that were returned by the query after query is run
    def deleteMultiple(self):
        url = self.query_data['URL']
        request = re.sub('sysparm_action=[^&]*', 'sysparm_action=%s' % 'deleteMultiple', url)
        self.post_url(request, json.dumps({
            'sysparm_query' : self.query_data['sysparm_query']
        }))

    #This is just a helper function
    #It refreshes the query string to contain most updated queries
    def refreshQuery(self):
        self.currentIndex = -1
        self.query_data['URL'] = re.sub('sysparm_action=[^&]*', 'sysparm_action=%s' % self.query_data['actionType'],
                                        self.query_data['URL'])
        self.query_data['URL'] = re.sub('sysparm_record_count=[^&]*', 'sysparm_record_count=%s' % self.query_data['rowCount'],
                                        self.query_data['URL'])

    #Returns the row to which cursor is currently pointing
    def getRow(self):
        rs = []
        for value in self.results[self.currentIndex].values():
            rs.append(str(value))
        return rs

    #Returns the headers of the table (i.e., names of the table columns)
    def getHeaders(self):
        rs = []
        for key in self.results[self.currentIndex].keys():
            rs.append(str(key))
        return rs

    #Makes the cursor move to the next record in the table
    def next(self):
        if self.currentIndex + 1 < self.getRowCount():
            self.currentIndex += 1
            return  True
        return  False

    #Adds a new query (filter) to the query string (e.g., addQuery("active", "true")
    def addQuery(self, key, value=""):
        if not self.query_data['sysparm_query']:
            self.query_data['sysparm_query'] = "%s=%s" % (key, value)
        else:
            self.query_data['sysparm_query'] += "^%s=%s" % (key, value)

        #print self.query_data

    #Queries ServiceNow, and stores the results in a variable, for future access
    def query(self):
        request = self.query_data['URL'] + self.query_data['sysparm_query']
        raw_json = self.get_url(request)
        #print raw_json.read()
        if raw_json:
            self.results = json.load(raw_json)['records']

    #This is just a helper function
    #Returns the request URL (excluding the query)
    def getQuery(self):
        return self.query_data['URL']

    #Limits the number of rows returned by queries (the default is 100 results per query)
    def setRowCount(self, n):
        self.query_data['rowCount'] = n
        self.refreshQuery()

    #Returns the number of table rows returned by the query
    def getRowCount(self):
        return len(self.results)

    #Clears all filters added to the query string
    def clearQuery(self):
        self.currentIndex = -1
        self.query_data['sysparm_query'] = ""

    #This function does a bunch of testing to make sure everything works as expected
    def unittest(self):
        def test_limited_retrieval():
            self.test_num += 1
            header = "\nTest %d: Testing retrieval of exactly 3 records" % self.test_num
            print header.ljust(70),
            self.clearQuery()
            self.setRowCount(3)
            self.addQuery("active", "true")
            self.query()

            if self.getRowCount() == 3:
                print "PASSED"
                return 1
            print "FAILED"
            print "*** After limiting rowCount to 3, we should get 3 records but" \
                  " %s records were returned ***\n" % (self.getRowCount())
            return 0


        def test_limited_update():
            self.test_num += 1
            header = "\nTest %d: Testing update of exactly 2 records" % self.test_num
            print header.ljust(70),

            #Get all records that were previously created using REST
            self.clearQuery()
            self.setRowCount("")
            self.addQuery("active", "true")
            self.addQuery("short_description", "Creating a record using GlideRecord API for Python")
            self.query()
            num_records = self.getRowCount()

            #update exactly 2 of them
            num_updated_records = 2
            self.clearQuery()
            self.setRowCount(num_updated_records)
            self.addQuery("active", "true")
            self.addQuery("short_description", "Creating a record using GlideRecord API for Python")
            self.setValues("short_description", "Updating a record using GlideRecord API for Python", False)

            #Now see if 2 of them are changed
            self.clearQuery()
            self.setRowCount("")
            self.addQuery("short_description", "Creating a record using GlideRecord API for Python")
            self.query()

            if self.getRowCount() == num_records - num_updated_records:
                print "PASSED"
                return 1
            print "FAILED"
            print "%s out of %s records were updated, %s should be left unchanged, but " \
                  "then number of unchanged records was %s" % \
                  (num_updated_records, num_records, num_records - num_updated_records, self.getRowCount())
            return 0

        def test_limited_deletion():
            self.test_num += 1
            header = "\nTest %d: Testing deletion of exactly 1 record" % self.test_num
            print header.ljust(70),

            #Get a subset of records using filters
            self.clearQuery()
            self.setRowCount("")
            self.addQuery("active", "true")
            self.addEncodedQuery("caller_idSTARTSWITHc")
            self.query()
            if self.hasNext():
                self.next()
            else:
                print "FAILED"
                print "*** Test failed because not records were returned, or there is something wrong" \
                      "with the 'hasNext()' function\n"
                return 0

            #delete one of them
            num_records = self.getRowCount()
            record_to_delete = self.getValue('number')
            self.clearQuery()
            self.setRowCount("")
            self.addQuery("number", record_to_delete)
            self.deleteMultiple()


            #See if record is deleted
            self.clearQuery()
            self.setRowCount("")
            self.addQuery("active", "true")
            self.addEncodedQuery("caller_idSTARTSWITHc")
            self.query()
            #Now let's see if exactly one record is deleted
            if self.getRowCount() == num_records - 1:
                print "PASSED"
                return 1
            print "FAILED"
            return 0

        def test_limited_insert():
            self.test_num += 1
            header = "\nTest %d: Testing insertion of exactly 3 new records" % self.test_num
            print header.ljust(70),

            #Getting all tickets that have a caller whose name starts with letter 'C'
            self.clearQuery()
            self.setRowCount("")
            self.addEncodedQuery("active=true^caller_idSTARTSWITHc")
            self.query()
            num_rows = self.getRowCount()

            #Inserting a new user whose name starts with letter 'C'
            record_info = {
                "caller_id": "Caitlin Roberts [caitlinr]",
                "u_phone_number": "123456",
                "u_service": "Quality Assurance",
                "short_description": "Creating a record using GlideRecord API for Python",
                "description": "ServiceNow GlideRecord API allows you to Create a record using Python",
                "assignment_group": "ServiceNow QA Team"
            }

            #Insert this record 3 times

            num_records_created = 3
            for i in range(num_records_created):
                self.insert(record_info)

            #Now let's see the number of such tickets is incremented by one
            self.clearQuery()
            self.setRowCount("")
            self.addEncodedQuery("active=true^caller_idSTARTSWITHc")
            self.query()
            if self.getRowCount() == num_rows + num_records_created:
                print "PASSED"
                return 1
            print "FAILED"
            print "*** After adding two new records, we should have %s records " \
                  "but had %s records ***\n" % (num_rows + 2, self.getRowCount())
            return 0

        #Deletes all records that were created during the test
        def delete_test_traces():
            time.sleep(1)
            self.test_num += 1
            header = "\nTest %d: Clearing traces of the tests (removing records created)" % self.test_num
            print header.ljust(70),
            self.clearQuery()
            self.addQuery("active", "true")
            self.addQuery("short_description", "Creating a record using GlideRecord API for Python")
            self.query()
            total_tickets_created = self.getRowCount()
            self.deleteMultiple()
            self.query()
            if self.getRowCount() == 0:
                print "PASSED"
                return 1
            print "FAILED"
            print "*** Not all of %d records were deleted ***\n" % total_tickets_created
            return 0


        #The main part of the testing is in below
        self.test_num = 0
        num_total_tests = 5
        num_passed_tests = 0
        num_passed_tests += test_limited_insert()
        num_passed_tests += test_limited_retrieval()
        num_passed_tests += test_limited_deletion()
        num_passed_tests += test_limited_update()
        num_passed_tests += delete_test_traces()

        print ""
        print "="*70
        print "All tests finished. Results: \r\n"
        print "Number of tests passed | Number of tests failed | Total number of tests |"
        print str(num_passed_tests).ljust(23) + "|" + str(num_total_tests - num_passed_tests).ljust(24) + "|" + str(num_total_tests).ljust(23) + "|"
        print "="*70

    #This is a helper function that is used to send GET, PUT or POST requests to Jira
    #This function is used by other functions and not the user directly
    def req_data(self, url, data, method):
        """Sends a request for data"""
        values = data
        url = re.sub('\s', '+', url)
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
                  "this user (%s) is Unauthorized to send REST requests or "
                  "request URL is not formatted correctly ***" % self.username)
            print("\n*** If username and password are correct, there is a chance this account is "
                  "blocked due to many unsuccessful login attempts ***")
            print(error)
            sys.exit(0)

        #print("Request was sent successfully.")

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
