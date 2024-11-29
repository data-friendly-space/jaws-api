# Query filtering
### Request
Send the three items together 
* Search term: Represent the value to be used as a filter
* Search field: the field that should be used in the query

### View
```python
def some_view(request):
    query_options = QueryOptions.from_request(request)
    response = some_service.get_some_data(query_options)
    return api_response("Success", response, 200)
```
### Service
```python
class SomeService():
    def __init__(self):
        self.some_repository = SomeRepository()

    def get_some_data(self, query_options: QueryOptions):
        return self.some_repository.get_some_data(query_options)
```
### Repository
```python
class SomeRepository():
    def get_some_data(self, query_options: QueryOptions):
        some_data_query = SomeModel.objects.all()

        some_data = query_options.filter_and_exec_queryset(some_data_query)

        return some_data
```

### Model
```python
class SomeData():
    id = UUIDField()
    name = CharField()
    lastname = CharField()
    email = CharField()
    age = DateTimeField()
```
## One field
For custom filter in your queries you should use the QueryOptions object this way
`/some_endpoint?search_term=test&search_fields=name`

## Multiple fields
You can achieve the same by adding more filters. The important thing here is to consider the order. You should keep together every group of filter (term, field and operator)

`/some_endpoint?search_fields=name&search_fields=email&search_term=some_email`
Here we have 2 filters. One filtering the `name` field with the `test` value using `contains`. The other filter uses the `email` field with the `some_email` value using `starts_with`.

# Pagination
Similar to the filtering, here you should send the `page_number` and `page_size` query params to make the pagination.
* page_number: the page you want to retrieve
* page_size: how many rows per page

`/some_endpoint?page_number=1&page_size=4`

# Ordering
Last but not least, to order the responses by a specific field you can use the query param `order_by`.
This receives a key value object.
* order_by: key value object
    * Key: the field you want to use in the orderign
    * Value: `asc` or `desc` depending on your requirements 

`/some_endpoint/order_by={"id":"desc"}`