from rest_framework.pagination import PageNumberPagination


class CoursePaginations(PageNumberPagination):
    page_size = 30
