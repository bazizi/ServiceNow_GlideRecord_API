ServiceNow GlideRecord API
==========================

####GlideRecord API for ServiceNow in Python


Sample:

```python
gr = GlideRecord("incident")

#Add search filters
gr.addQuery("active", "true")
gr.addEncodedQuery('caller_id=76239f4b875a78006fa670406d434d39')

#Limit the number of results, to avoid making the server unnecessarily busy (The default is 100 results per query)
#gr.setRowCount(1)

#Query ServiceNow
#gr.query()

while gr.next():
    print gr.getRow()
    print "\r\n"

```
