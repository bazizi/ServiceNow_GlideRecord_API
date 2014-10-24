ServiceNow GlideRecord API
==========================
Using ServiceNow GlideRecord API in Python you can run GlideRecord commands right from your own computer and/or automate ServiceNow tasks.

Current capabilities are:
- Query records using filters (sysparm_query)
- Create new records in any given table on ServiceNow
- Update existing records
- Remove a record or a set of records all at once, using filters

###GlideRecord API for ServiceNow in Python


####Examples:

#####Read data in a table, using filters:

```python
from GlideRecord import *

#Set which table to query
gr = GlideRecord("incident")

#Set the url to the server were the ServiceNow instance is
gr.set_server("https://sfustg.service-now.com/")

#Set user credentials to send REST requests
#One of the next two lines should be commented
#Comment the first one if: You will want to provide username/password from command line (recommended)
#Comment the second on if: You want to provide username/password in plain text (not recommended)
gr.get_credentials()
#gr.set_credentials("YOUR USERNAME GOES HERE", "YOUR PASSWORD GOES HERE")

#Add search filters
gr.addQuery("active", "true")
gr.addEncodedQuery('caller_id=76239f4b875a78006fa670406d434d39')

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

```

#####Delete a set of records returned by a filter:

```python
from GlideRecord import *

#Set which table to query
gr = GlideRecord("incident")

#Set the url to the server were the ServiceNow instance is
gr.set_server("https://sfustg.service-now.com/")

#Set user credentials to send REST requests
#One of the next two lines should be commented
#Comment the first one if: You will want to provide username/password from command line (recommended)
#Comment the second on if: You want to provide username/password in plain text (not recommended)
gr.get_credentials()
#gr.set_credentials("YOUR USERNAME GOES HERE", "YOUR PASSWORD GOES HERE")

#Add search filters
gr.addQuery("active", "true")
gr.addEncodedQuery('caller_id=76239f4b875a78006fa670406d434d39')

gr.deleteMultiple()


```

#####Create a new record:

```python
#Set which table to query
gr = GlideRecord("incident")

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

gr.insert(record_info)

```
