ServiceNow GlideRecord API
==========================

####GlideRecord API for ServiceNow in Python


#####Examples:

Query a table using filters:

```python
gr = GlideRecord("incident")

#Add search filters
gr.addQuery("active", "true")
gr.addEncodedQuery('caller_id=76239f4b875a78006fa670406d434d39')

#Limit the number of results, to avoid making the server unnecessarily busy (The default is 100 results per query)
gr.setRowCount(1)

#Query ServiceNow
gr.query()

while gr.next():
    print gr.getRow()
    print "\r\n"

```

Delete a set of records returned by a filter:

```python
gr = GlideRecord("incident")

#Add search filters
gr.addQuery("active", "true")
gr.addEncodedQuery('caller_id=76239f4b875a78006fa670406d434d39')
gr.deleteMultiple()

```

Create a new record:

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
