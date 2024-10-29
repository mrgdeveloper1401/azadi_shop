from rest_framework.pagination import PageNumberPagination


class UserAdminPagination(PageNumberPagination):
    page_size = 30
