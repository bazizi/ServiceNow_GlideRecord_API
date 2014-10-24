from __init__ import *

#Set which table to query
gr = GlideRecord("incident")

#Set the url to the server were the ServiceNow instance is
gr.set_server("https://sfustg.service-now.com/")

#Set user credentials to send REST requests
#This can be done either by entering username password in the command line (recommended):
gr.get_credentials()
#-- OR -- Can be done by storing the username/passowrd in plain text (not recommended)
#This can be done either through the code (not recommended):
#gr.set_credentials("YOUR USERNAME GOES HERE", "YOUR PASSWORD GOES HERE")

#Add search filters
gr.addQuery("active", "true")
#gr.addEncodedQuery('caller_id=76239f4b875a78006fa670406d434d39')

#Limit the number of results, to avoid making the server unnecessarily busy (The default is 100 results per query)
gr.setRowCount(1)

#Query ServiceNow
gr.query()

#How many rows returned?
print "Number of results: %s" % gr.getRowCount()

#While the cursor has not reached end of the results
while gr.next():
    print gr.getRow()
    print "\r\n"



"""
record_info = """
"""

gr.insert()
"""

#Sets the value of all phone numbers (that are returned by the above queries)
#gr.setValues('u_phone_number', '12345')


#gr.deleteMultiple()













