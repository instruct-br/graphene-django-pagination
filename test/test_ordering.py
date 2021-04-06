from unittest.mock import Mock
from graphene_django_pagination.connection_field import connection_from_list_ordering


def test_connection_from_list_ordering():
    mock_items_list = Mock()
    mock_items_list.order_by.return_value = []
    ordering = 'name,asc'

    items_list_sorted = connection_from_list_ordering(
        mock_items_list,
        ordering
    )

    assert items_list_sorted == []
