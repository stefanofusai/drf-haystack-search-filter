# drf-haystack-search-filter

A [django-haystack](https://github.com/django-haystack/django-haystack) search filter for Django Rest Framework.

This package uses [uv](https://docs.astral.sh/uv/) for project management. To get started, ensure that **uv** is installed on your machine and updated to the latest version. Detailed installation instructions for **uv** can be found [here](https://docs.astral.sh/uv/getting-started/installation/).

## Installation

```bash
uv add drf-haystack-search-filter
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

## Development

```bash
uv sync --frozen --group=development
uv run --frozen pre-commit install --install-hooks
uv run --frozen pre-commit install --hook-type=commit-msg
```

## Contributing

Contributions are welcome! To get started, please refer to our [contribution guidelines](https://github.com/stefanofusai/drf-haystack-search-filter/blob/main/CONTRIBUTING.md).

## Issues

If you encounter any problems while using this package, please open a new issue [here](https://github.com/stefanofusai/drf-haystack-search-filter/issues).
