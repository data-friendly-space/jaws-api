import ast
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from rest_framework import serializers


class QueryOptions(serializers.Serializer):
    page_number = serializers.IntegerField(required=False)
    page_size = serializers.IntegerField(required=False)
    search_terms = serializers.ListField(child=serializers.CharField(), required=False)
    search_fields = serializers.ListField(child=serializers.CharField(), required=False)
    search_operators = serializers.ListField(child=serializers.CharField(), required=False)
    order_by = serializers.DictField(child=serializers.CharField(), required=False)

    def __init__(self, page_number=None, page_size=None, search_terms=None, search_fields=None, search_operators=None,
                 order_by=None):
        super().__init__()
        self.page_number = page_number
        self.page_size = page_size
        self.search_terms = search_terms
        self.search_fields = search_fields
        self.search_operators = search_operators
        self.order_by = order_by

    def to_dict(self):
        return {
            'page_number': self.page_number,
            'page_size': self.page_size,
            'search_terms': self.search_terms,
            'search_fields': self.search_fields,
            'search_operators': self.search_operators,
            'order_by': self.order_by
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            page_number=data.get('page_number'),
            page_size=data.get('page_size'),
            search_terms=data.get('search_terms'),
            search_fields=data.get('search_fields'),
            search_operators=data.get('search_operators'),
            order_by=data.get('order_by')
        )

    @classmethod
    def from_request(cls, request):
        order_by = request.query_params.get('order_by')
        if order_by:
            order_by = ast.literal_eval(order_by)

        return cls(
            page_number=request.query_params.get('page_number'),
            page_size=request.query_params.get('page_size'),
            search_terms=request.query_params.getlist('search_terms'),
            search_fields=request.query_params.getlist('search_fields'),
            search_operators=request.query_params.getlist('search_operators'),
            order_by=order_by
        )

    def filter_and_exec_queryset(self, queryset: QuerySet) -> list:
        if not queryset:
            return list()

        if self.search_terms and self.search_fields and self.search_operators:
            search_filter = Q()
            for term, field, operator in zip(self.search_terms, self.search_fields, self.search_operators):
                search_filter |= Q(**{f'{field}__{operator}': term})
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
