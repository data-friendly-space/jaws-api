"""This module contains the query options"""
import ast
from typing import List, Optional, Type
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet, Model
from rest_framework import serializers


class QueryOptions(serializers.Serializer):
    """Class for handling the querying, ordering and pagination"""
    page_number = serializers.IntegerField(required=False)
    page_size = serializers.IntegerField(required=False)
    search_term = serializers.CharField(required=False)
    search_fields = serializers.ListField(child=serializers.CharField(), required=False)
    order_by = serializers.DictField(child=serializers.CharField(), required=False)
    filters = serializers.DictField(child=serializers.CharField(), required=False)
    def __init__(self,
                 page_number=None,
                 page_size=None,
                 search_term=None,
                 search_class=None,
                 search_fields=None,
                 order_by=None,
                 filters=None):
        super().__init__()
        self.page_number = page_number
        self.page_size = page_size
        self.search_term = search_term
        self.search_class = search_class
        self.search_fields = search_fields
        self.order_by = order_by
        self.filters = filters or {}

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

        filters = request.query_params.get('filters')
        if filters:
            filters = ast.literal_eval(filters)

        return cls(
            page_number=request.query_params.get('page_number'),
            page_size=request.query_params.get('page_size'),
            search_term=request.query_params.get('search_term'),
            order_by=order_by,
            filters=filters  # Nuevo
        )

    def get_queryable_fields(self, model: Type[Model], include_relations=False) -> List[str]:
        """
        Get fields of the model that can be queried.
        Includes related fields if specified.
        """
        fields = []
        for field in model._meta.get_fields(include_parents=True):
            if include_relations and field.is_relation:
                # Recursively fetch related model fields for nested queries
                related_model = field.related_model
                if related_model:
                    related_fields = [
                        f"{field.name}__{related_field.name}"  # Example: user__name
                        for related_field in related_model._meta.get_fields()
                        if not (related_field.is_relation or related_field.many_to_many)
                    ]
                    fields.extend(related_fields)
            elif not field.is_relation:  # Include only non-relational fields
                fields.append(field.name)
        return fields

    def filter_and_exec_queryset(
            self,
            queryset: QuerySet,
            model: Type[Model],
            exclude_fields: Optional[List[str]] = None) -> dict:
        """Filter, order and paginate the response directly in SQL query, including total records."""
        if not queryset.exists():  # Check if queryset has records
            return {"total": 0, "results": []}

        # Determine searchable fields
        self.search_fields = self.search_fields or [
            field.name for field in model._meta.get_fields()
            if not (field.is_relation or field.many_to_one or field.many_to_many)
        ]

        # Exclude specific fields
        if exclude_fields:
            self.search_fields = [
                field for field in self.search_fields if field not in exclude_fields
            ]

        # Filter by searchTerm
        if self.search_term and self.search_fields:
            search_filter = Q()
            for field in self.search_fields:
                search_filter |= Q(**{f'{field}__icontains': self.search_term})
            queryset = queryset.filter(search_filter)

        # Advanced custom filters
        if self.filters:
            for key, value in self.filters.items():
                queryset = queryset.filter(**{key: value})

        # Order by nested fields
        if self.order_by:
            ordering = []
            for field, direction in self.order_by.items():
                if direction not in ['asc', 'desc']:
                    continue
                ordering.append(field if direction == 'asc' else f'-{field}')
            if ordering:
                queryset = queryset.order_by(*ordering)

        # Get total count BEFORE applying pagination
        total_count = queryset.count()

        # Pagination directly in the database using LIMIT and OFFSET
        page = int(self.page_number or 0)  # Default to page 1
        page_size = int(self.page_size or 10)  # Default to 10 items per page
        offset = page * page_size  # Calculate the offset

        # Apply pagination
        paginated_queryset = queryset[offset:offset + page_size]

        # Return both results and total count
        return {
            "total": total_count,  # Total number of records without pagination
            "results": list(paginated_queryset)  # Paginated results
        }
