"""This module contains the query options"""
import ast
from math import ceil
from typing import List, Optional, Type
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet, Model
from pandas import DataFrame
from rest_framework import serializers


class QueryOptions(serializers.Serializer):
    """Class for handling the querying, ordering and pagination"""
    page_number = serializers.IntegerField(required=False)
    page_size = serializers.IntegerField(required=False)
    search_term = serializers.CharField(required=False)
    search_fields = serializers.ListField(child=serializers.CharField(), required=False)
    order_by = serializers.DictField(child=serializers.CharField(), required=False)

    def __init__(self,
                 page_number=None,
                 page_size=None,
                 search_term=None,
                 search_class=None,
                 search_fields=None,
                 order_by=None):
        super().__init__()
        self.page_number = page_number
        self.page_size = page_size
        self.search_term = search_term
        self.search_class = search_class
        self.search_fields = search_fields
        self.order_by = order_by

    def to_dict(self):
        """Return a dict of the query options"""
        return {
            'page_number': self.page_number,
            'page_size': self.page_size,
            'search_term': self.search_term,
            'search_fields': self.search_fields,
            'order_by': self.order_by
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a QueryOption from a dict"""
        return cls(
            page_number=data.get('page_number'),
            page_size=data.get('page_size'),
            search_term=data.get('search_term'),
            search_fields=data.get('search_fields'),
            order_by=data.get('order_by')
        )

    @classmethod
    def from_request(cls, request):
        """Creates a query option from a request"""
        order_by = request.query_params.get('order_by')
        if order_by:
            order_by = ast.literal_eval(order_by)

        return cls(
            page_number=request.query_params.get('page_number'),
            page_size=request.query_params.get('page_size'),
            search_term=request.query_params.get('search_term'),
            order_by=order_by
        )

    def get_queryable_fields(self, model: Type[Model]) -> List[str]:
        """
        Get fields of the model that can be queried (non-relational fields).
        """
        return [
            field.name
            for field in model._meta.get_fields(include_parents=True)
            if not (field.is_relation or field.many_to_one or field.many_to_many)
        ]

    def filter_and_exec_queryset(
            self,
            queryset: QuerySet,
            model: Type[Model],
            exclude_fields: Optional[List[str]] = None) -> list:
        """Filter, order and paginate the response"""
        if not queryset:
            return list()

        self.search_fields = self.get_queryable_fields(model)

        if exclude_fields:
            self.search_fields = [
                field for field in self.search_fields if field not in exclude_fields
            ]

        if self.search_term and self.search_fields:
            search_filter = Q()
            for field in self.search_fields:
                search_filter |= Q(**{f'{field}__icontains': self.search_term})
            queryset = queryset.filter(search_filter)

        if self.order_by:
            ordering = []
            for field, direction in self.order_by.items():
                if direction not in ['asc', 'desc']:
                    continue
                ordering.append(field if direction == 'asc' else f'-{field}')
            if ordering:
                queryset = queryset.order_by(*ordering)

        if self.page_number and self.page_size:
            paginator = Paginator(queryset, self.page_size)
            page = paginator.get_page(self.page_number)
            return page.object_list
        else:
            return list(queryset)

    def paginate_and_filter_dataframe(self, dataframe: DataFrame):
        """Return the specified rows of a dataframe"""
        page_number = max(int(self.page_number), 1)
        page_size = max(int(self.page_size), 1)

        if self.search_term:
            dataframe = dataframe[
                dataframe.apply(
                    lambda row: row.astype(str).str.contains(
                        self.search_term, case=False
                    ).any(), axis=1
                )
            ]

        if self.order_by:
            for column, direction in self.order_by.items():
                dataframe = dataframe.sort_values(
                    by=column, ascending=(direction.lower() == 'asc')
                )

        total_records = len(dataframe)
        total_pages = ceil(total_records / page_size)
        total_columns = len(dataframe.columns)

        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = dataframe.iloc[start_idx:end_idx]

        return {
            "data": paginated_data,
            "totalRows": total_records,
            "totalColumns": total_columns,
            "totalPages": total_pages,
            "currentPage": page_number,
            "pageSize": page_size,
        }
