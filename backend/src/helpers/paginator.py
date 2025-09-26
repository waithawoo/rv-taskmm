from math import ceil
from typing import List, Any


class Paginator:
    def __init__(self, items: List[Any], total: int, page: int, per_page: int):
        self.items = items
        self.total = total
        self.page = page
        self.per_page = per_page
        self.total_pages = ceil(total / per_page)

    def to_dict(self):
        return {
            'total': self.total,
            'page': self.page,
            'per_page': self.per_page,
            'total_pages': self.total_pages,
        }


class CursorPaginator:
    def __init__(self, items, limit, has_next, next_cursor):
        self.items = items
        self.limit = limit
        self.has_next = has_next
        self.next_cursor = next_cursor

    def to_dict(self):
        return {
            'limit': self.limit,
            'has_next': self.has_next,
            'next_cursor': self.next_cursor,
        }
