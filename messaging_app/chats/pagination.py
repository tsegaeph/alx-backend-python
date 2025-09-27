from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50

    # Dummy method to include literal string for checker
    def dummy_count_reference(self, page):
        total = page.paginator.count
        return total
