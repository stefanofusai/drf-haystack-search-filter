from typing import TypeVar

from django.db.models import QuerySet
from haystack.query import SearchQuerySet
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.views import APIView

T = TypeVar("T")


class HaystackSearchFilter(SearchFilter):
    """A search filter for Django Rest Framework that uses Django Haystack's search indexes."""  # noqa: E501

    def filter_queryset(  # noqa: D102
        self, request: Request, queryset: QuerySet[T], view: APIView
    ) -> QuerySet[T]:
        # Avoid search form not being rendered in DRF's Browsable API
        # (if not getattr(view, 'search_fields', None): return ''),
        # since HaystackSearchFilter uses Django Haystack's search indexes
        # rather than standard Django ORM fields.
        if getattr(view, "search_fields", None) is None:
            view.search_fields = ["__all__"]  # this can contain anything

        query = request.query_params.get(self.search_param)

        if query is None:
            return queryset

        return self._search(request, queryset, view, query)

    def _search(
        self, request: Request, queryset: QuerySet[T], view: APIView, query: str
    ) -> QuerySet[T]:
        """A method that can be overridden to customize the search behavior.

        :param request: The request object.
        :type request: Request
        :param queryset: The queryset to filter.
        :type queryset: QuerySet[T]
        :param view: The view object.
        :type view: APIView
        :param query: The search query.
        :type query: str
        :return: The filtered queryset.
        :rtype: QuerySet[T]
        """  # noqa: D401
        return queryset.filter(
            pk__in=(
                SearchQuerySet()
                .models(queryset.model)
                .filter(content__startswith=query)
                .values_list("pk", flat=True)
            )
        )
