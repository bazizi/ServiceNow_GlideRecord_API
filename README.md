ServiceNow GlideRecord API
==========================
Using ServiceNow GlideRecord API in Python you can run GlideRecord commands right from your own computer and/or automate ServiceNow tasks.

Current capabilities are:
- Query records using filters (sysparm_query)
- Create new records in any given table on ServiceNow
- Update existing records
- Remove a record or a set of records all at once, using filters

###GlideRecord API for ServiceNow in Python
####Installation:
#####Using PIP (Recommended)
If your version of Python supports PIP package manager, installation is as simple as running this command:

*pip install GlideRecord*

If not, it is recommended that you install pip from the following URL, and retry the above command:
http://pip.readthedocs.org/en/latest/installing.html

#####Manual installation using Git
If you have Git, you can install GlideRecord API by running these commands in order:
- *git clone https://github.com/bazizi/ServiceNow_GlideRecord_API.git*
- *cd ServiceNow_GlideRecord_API*
- *python setup.py install*

#####Need help?
If you need any help regarding installation and/or usage of GlideRecord API, feel free to contact me via my email: b.a

####Examples:

#####Read data in a table, using filters:
The below code snippet **reads** records stored in the 'incident' table that have status 'active' and are created by someone with a specific caller ID.
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
<br />

#####Delete a set of records returned by a filter:
The below code snippet **deletes** all 'incident' records  that status 'active' and have the specified caller ID.

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
<br />


#####Insert a new record into any given table:
The below code snippet **inserts** a new record into the 'incident' table, using the specified values.
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

record_info = {
    "caller_id" : "James Bond [jbond]",
    "u_phone_number" : "123456",
    "u_service" : "Quality Assurance",
    "short_description" : "Creating a record using GlideRecord API for Python",
    "description" : "ServiceNow GlideRecord API allows you to Create a record using Python", 
    "assignment_group" : "ServiceNow QA Team"
}

gr.insert(record_info)

```

####Available Member Functions:
| Funcation name  | Description  | Example |
|---|---|---|
| set\_server(server\_name) | Used to indicate which server to query | set\_server("ubc.service-now.com") |
| set\_credentials(username, password) | Used to indicate which username/password is used to query ServiceNow| set\_credentials("hpotter", "somepassword") |
| get\_credentials() | When this function is called, user credentials are read from command line | get\_credentials() |
| addQuery(key, value) | Adds a filter to the query | addQuery("active", "true") |
| addEncodedQuery(filter) | Used to add a sysparm_query to the GlideRecord | addEncodedQuery("active=true") |
| query()  | queries the table  | query() |
| next() | returns 'true' if cursor has not reached the end of results | while gr.next(): print gr.getRow() |
| insert(json\_data) | used to insert a new record into a table | insert(\{"u\_phone_number":"12345"\}) |
| deleteMultiple() | used to delete all records that match the queries | deleteMultiple() |
| setValues(key, value) | Sets the values of cells in a column | setValues('u\_phone\_number', '12345') |
| delete() | Delete a single record. The syparm_sys_id of the record needs to be added to query beforehand | delete() |
| getValue(key) | Get the value of a cell in the row where cursor is pointing | getValue('u\_phone\_number') |
==============================================================================================
###License Information:

The MIT License (MIT)<br />
Copyright (c) 2014 Behnam Azizi<br />
Permission is hereby granted, free of charge, to any person obtaining a copy<br />
of this software and associated documentation files (the "Software"), to deal<br />
in the Software without restriction, including without limitation the rights<br />
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell<br />
copies of the Software, and to permit persons to whom the Software is<br />
furnished to do so, subject to the following conditions:<br />
The above copyright notice and this permission notice shall be included in all<br />
copies or substantial portions of the Software.<br />
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR<br />
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,<br />
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE<br />
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER<br />
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,<br />
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE<br />
SOFTWARE.
