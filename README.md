# graphene-django-pagination

This package adds offset-based pagination to [Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/) without using [Graphene Relay](https://docs.graphene-python.org/en/latest/relay/).

## Installation

Using [Pipenv:](https://github.com/pypa/pipenv)

    $ pipenv install https://github.com/instruct-br/graphene-django-pagination/archive/master.zip

## Documentation

**Fields:**

**DjangoPaginationConnectionField**

- 1. It allows paginate the query using offset-based method and returns the `totalCount` field that indicates the total query results.
- 2. Also, it is possible to order list using the pattern `input,enum` just sendind `ordering` field.

## Example

#### 1 - Model (models.py)

```python
from django.db import models


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
```

#### 2 - Type (types.py)

```python
from graphene_django.types import DjangoObjectType
from .models import Customer


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filter_fields = {
            "name": ["istartswith", "exact"]
        }
```

#### 3 - Schema (schema.py)

```python
from graphene_django_pagination import DjangoPaginationConnectionField
from graphene import ObjectType
from .types import CustomerType
from .models import Customer


class Query(ObjectType):
    customers = DjangoPaginationConnectionField(CustomerType)

    def resolve_customers(self, info, **kwargs):
        return Customer.objects.all()
```

#### 4 - Queries

##### 4.1 - Query without limit, offset and filter

```graphql
query customers {
  customers {
    totalCount
    results {
      id
      name
    }
  }
}
```

```json
{
    "data": {
        "customers": {
            "totalCount": 6,
            "results": [
                {
                    "id": 1,
                    "name": "Figo"
                },
                {
                    "id": 2,
                    "name": "Edson Arantes do Nascimento"
                }
                {
                    "id": 3,
                    "name": "Lionel Messi"
                }
                {
                    "id": 4,
                    "name": "Ibrahimović"
                }
                {
                    "id": 5,
                    "name": "Paul Pogba"
                }
                {
                    "id": 6,
                    "name": "Eden Hazard"
                }
            ]
        }
    }
}
```

##### 4.2 - Query with only limit and offset

```graphql
query customers {
  customers(limit: 3, offset: 0) {
    totalCount
    results {
      id
      name
    }
  }
}
```

```json
{
  "data": {
    "customers": {
      "totalCount": 6,
      "results": [
        {
          "id": 1,
          "name": "Figo"
        },
        {
          "id": 2,
          "name": "Edson Arantes do Nascimento"
        },
        {
          "id": 3,
          "name": "Lionel Messi"
        }
      ]
    }
  }
}
```

##### 4.3 - Query with limit, offset and filter

```graphql
query customers {
  customers(limit: 3, offset: 0, nickname_Istartswith: "E") {
    totalCount
    results {
      id
      name
    }
  }
}
```

```json
{
  "data": {
    "customers": {
      "totalCount": 2,
      "results": [
        {
          "id": 2,
          "name": "Edson Arantes do Nascimento"
        },
        {
          "id": 6,
          "name": "Eden Hazard"
        }
      ]
    }
  }
}
```

##### 4.4 - Query with ordering

```graphql
query customers {
  customers(ordering: "name,asc") {
    totalCount
    results {
      id
      name
    }
  }
}
```

```json
{
  "data": {
    "customers": {
        "totalCount": 6,
        "results": [
          {
            "id": 6,
            "name": "Eden Hazard"
          },
          {
            "id": 2,
            "name": "Edson Arantes do Nascimento"
          },
          {
            "id": 1,
            "name": "Figo"
          },
          {
            "id": 4,
            "name": "Ibrahimović"
          },
          {
            "id": 3,
            "name": "Lionel Messi"
          }
          {
            "id": 5,
            "name": "Paul Pogba"
          }
        ]
    }
  }
}
```

##### 4.5 - Query with ordering, limit and offset

```graphql
query customers {
  customers(ordering: "id,desc", limit: 3, offset: 0) {
    totalCount
    results {
      id
      name
    }
  }
}
```

```json
{
  "data": {
    "customers": {
      "totalCount": 6,
      "results": [
        {
          "id": 6,
          "name": "Eden Hazard"
        },
        {
          "id": 5,
          "name": "Paul Pogba"
        },
        {
          "id": 4,
          "name": "Ibrahimović"
        }
      ]
    }
  }
}
```
