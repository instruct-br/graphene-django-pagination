import re
import math

from graphene import Int, String
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.utils import maybe_queryset
from django.core.paginator import Paginator
from django.db.models.query import QuerySet

from . import PaginationConnection, PageInfoExtra


class DjangoPaginationConnectionField(DjangoFilterConnectionField):
    def __init__(
        self,
        type,
        fields=None,
        order_by=None,
        extra_filter_meta=None,
        filterset_class=None,
        *args,
        **kwargs
    ):
        self._type = type
        self._fields = fields
        self._provided_filterset_class = filterset_class
        self._filterset_class = None
        self._extra_filter_meta = extra_filter_meta
        self._base_args = None

        kwargs.setdefault("limit", Int(description="Query limit"))
        kwargs.setdefault("offset", Int(description="Query offset"))
        kwargs.setdefault("ordering", String(description="Query order"))

        super(DjangoPaginationConnectionField, self).__init__(
            type,
            *args,
            **kwargs
        )

    @property
    def type(self):

        class NodeConnection(PaginationConnection):
            total_count = Int()

            class Meta:
                node = self._type
                name = '{}NodeConnection'.format(self._type._meta.name)

            def resolve_total_count(self, info, **kwargs):
                return self.iterable.count()

        return NodeConnection

    @classmethod
    def resolve_connection(cls, connection, default_manager, args, iterable):
        if iterable is None:
            iterable = default_manager

        iterable = maybe_queryset(iterable)

        if isinstance(iterable, QuerySet):
            if iterable.model.objects is not default_manager:
                default_queryset = maybe_queryset(default_manager)
                iterable = cls.merge_querysets(default_queryset, iterable)

            _len = iterable.count()
        else:
            _len = len(iterable)

        ordering = args.get("ordering")

        if ordering:
            iterable = connection_from_list_ordering(iterable, ordering)

        connection = connection_from_list_slice(
            iterable,
            args,
            connection_type=connection,
            pageinfo_type=PageInfoExtra,
        )
        connection.iterable = iterable
        connection.length = _len

        return connection


def connection_from_list_slice(
    list_slice, args=None, connection_type=None, pageinfo_type=None
):
    args = args or {}
    limit = args.get("limit", None)
    offset = args.get("offset", 0)

    if limit is None:
        return connection_type(
            results=list_slice,
            page_info=pageinfo_type(
                has_previous_page=False,
                has_next_page=False
            )
        )
    else:
        assert isinstance(limit, int), "Limit must be of type int"
        assert limit > 0, "Limit must be positive integer greater than 0"

        paginator = Paginator(list_slice, limit)
        _slice = list_slice[offset:(offset+limit)]

        page_num = math.ceil(offset/limit) + 1
        page_num = (
            paginator.num_pages
            if page_num > paginator.num_pages
            else page_num
        )
        page = paginator.page(page_num)

        return connection_type(
            results=_slice,
            page_info=pageinfo_type(
                has_previous_page=page.has_previous(),
                has_next_page=page.has_next()
            )
        )


def connection_from_list_ordering(items_list, ordering):
    field, order = ordering.split(',')

    order = '-' if order == 'asc' else ''
    field = re.sub(r'(?<!^)(?=[A-Z])', '_', field).lower()

    return items_list.order_by(f'{order}{field}')
