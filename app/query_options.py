'''This module contains the query options'''
import ast
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from rest_framework import serializers


class QueryOptions(serializers.Serializer):
    '''Class for handling the querying, ordering and pagination'''
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
        '''Return a dict of the query options'''
        return {
            'page_number': self.page_number,
            'page_size': self.page_size,
            'search_term': self.search_term,
            'search_fields': self.search_fields,
            'order_by': self.order_by
        }

    @classmethod
    def from_dict(cls, data):
        '''Creates a QueryOption from a dict'''
        return cls(
            page_number=data.get('page_number'),
            page_size=data.get('page_size'),
            search_term=data.get('search_term'),
            search_fields=data.get('search_fields'),
            order_by=data.get('order_by')
        )

    @classmethod
    def from_request(cls, request):
        '''Creates a query option from a request'''
        order_by = request.query_params.get('order_by')
        if order_by:
            order_by = ast.literal_eval(order_by)

        return cls(
            page_number=request.query_params.get('page_number'),
            page_size=request.query_params.get('page_size'),
            search_term=request.query_params.get('search_term'),
            search_fields=request.query_params.getlist('search_fields'),
            order_by=order_by
        )

    def filter_and_exec_queryset(self, queryset: QuerySet) -> list:
        '''Filter, order and paginate the response'''
        if not queryset:
            return list()

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
