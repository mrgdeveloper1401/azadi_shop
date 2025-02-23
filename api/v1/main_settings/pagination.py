from rest_framework import pagination


class TopTeacherPagination(pagination.PageNumberPagination):
    page_size = 5
