from unittest import TestCase
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range, make_pagination


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_start_range_adjustment(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_stop_range_adjustment(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=3,
            current_page=4
        )['pagination']
        self.assertEqual([4, 5, 6], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3
        )['pagination']
        self.assertEqual([2, 3, 4, 5, 6], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4
        )['pagination']
        self.assertEqual([3, 4, 5, 6, 7], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10
        )['pagination']
        self.assertEqual([9, 10, 11, 12, 13], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12
        )['pagination']
        self.assertEqual([11, 12, 13, 14, 15], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_middle_range_adjustment(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=10
        )['pagination']
        self.assertEqual([9, 10, 11, 12, 13], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=12
        )['pagination']
        self.assertEqual([11, 12, 13, 14, 15], pagination)

    def test_pagination_at_the_end(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_edge_case_when_qty_pages_greater_than_total_pages(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 6)),
            qty_pages=10,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4, 5], pagination)

    def test_invalid_current_page(self):
        class FakeRequest:
            GET = {'page': 'invalid'}

        request = FakeRequest()
        queryset = list(range(1, 21))  # Dummy queryset
        page_obj, pagination = make_pagination(request, queryset, 5)
        self.assertEqual(page_obj.number, 1)
        # Convert the range to a list for comparison
        self.assertEqual(list(pagination['pagination']), [1, 2, 3, 4])
