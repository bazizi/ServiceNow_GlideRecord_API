
"""
    Author: 
            Behnam Azizi
            cgi.sfu.ca/~bazizi

    Date: 
        Oct. 11, 2014

    Description: 
        ServiceNow Rest API (GlideRecord) for Python
        Based on ServiceNow GlideRecord documentation:
            http://wiki.servicenow.com/index.php?title=GlideRecord
"""

from __init__ import *

#========================== Methods and Initializers ===============================

#==================================================================

#Set which table to query
gr = GlideRecord("incident")

#Add search filters
gr.addQuery("active", "true")
gr.addQuery("caller_id", "76239f4b875a78006fa670406d434d39")
#gr.addQuery("")
#gr.addEncodedQuery('caller_id=76239f4b875a78006fa670406d434d39')

gr.comments = "hello"

record_info = """
{
    "caller_id" : "James Bond [jbond]",
    "u_phone_number" : "12345",
    "u_service" : "Quality Assurance",
    "short_description" : "Creating a record using GlideRecord API for Python",
    "description" : "ServiceNow GlideRecord API allows you to Create a record using Python", 
    "assignment_group" : "ServiceNow QA Team"
}
"""

gr.insert()

#Limit the number of results, to avoid making the server unnecessarily busy (The default is 100 results per query)
#gr.setRowCount(1)

#gr.deleteMultiple()
#Query ServiceNow
#gr.query()


"""
#How many rows returned?
print "Number of results: %s" % gr.getRowCount()

#Sets the value of all phone numbers (that are returned by the above queries)
#gr.setValues('u_phone_number', '12345')

#While the cursor has not reached end of the results
while gr.next():
    print gr.getRow()
    print "\r\n"
"""