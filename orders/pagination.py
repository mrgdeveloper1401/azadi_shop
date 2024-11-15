from rest_framework.pagination import PageNumberPagination


class OrdersPageNumberPagination(PageNumberPagination):
    page_size = 20
