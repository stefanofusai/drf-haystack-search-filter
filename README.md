# drf-haystack-search-filter

A simple package to implement a [django-haystack](https://github.com/django-haystack/django-haystack) search filter in Django Rest Framework.

## Installation

```bash
pip install drf-haystack-search-filter
```

## Usage

Simply import the `HaystackSearchFilter` and use it in your API views:

```python
from drf_haystack_search_filter.filters import HaystackSearchFilter

...

class MyAPIView(...):
    ...
    filter_backends = [HaystackSearchFilter, ...]
    ...
```

You can customize the search behavior by overriding the `_search` method.

```python
from typing import TypeVar

from drf_haystack_search_filter import HaystackSearchFilter

T = TypeVar("T")


class MyHaystackSearchFilter(HaystackSearchFilter):
    def _search(self, request: Request, queryset: QuerySet[T], view: APIView, query: str) -> QuerySet[T]:
        # Customize the search behavior here
        return queryset.filter(
            pk__in=(
                SearchQuerySet()
                .models(queryset.model)
                .filter(content__startswith=query)
                .values_list("pk", flat=True)
            )
        )

class MyAPIView(...):
    ...
    filter_backends = [MyHaystackSearchFilter, ...]
    ...
```

## Contributing

Contributions are welcome! To get started, please refer to our [contribution guidelines](https://github.com/stefanofusai/drf-haystack-search-filter/blob/main/CONTRIBUTING.md).

## Issues

If you encounter any problems while using this package, please open a new issue [here](https://github.com/stefanofusai/drf-haystack-search-filter/issues).
