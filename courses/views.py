from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from courses.permissions import IsAuthenticatedOrAdmin, IsOwner
from courses.paginations import CoursePagination
from courses.serializers import CommentSerializers, CourseSerializers, CourseDiscountSerializers, CategorySerializers, \
    CreatCommentSerializer
from courses.models import CourseCategory, Course, DiscountCourse, Comment
from courses.filters import CourseFilter


class CategoryListAPIView(ReadOnlyModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializers


class CourseViewSet(ReadOnlyModelViewSet):
    serializer_class = CourseSerializers
    queryset = Course.objects.select_related('user', "category")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['name']
    ordering_fields = ['course_discount', 'updated_at', 'created_at']
    pagination_class = CoursePagination
    lookup_field = 'slug'


class DiscountCourseApiView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = DiscountCourse.objects.select_related('course').all()
    serializer_class = CourseDiscountSerializers


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"course_slug": self.kwargs['course_slug'], "request": self.request}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatCommentSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Comment.objects.filter(course__slug=self.kwargs['course_slug']).select_related("user", "course")
