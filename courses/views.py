from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import NotAcceptable
from django.db.models import Case, When, F, DecimalField, Value

from courses.permissions import IsOwner
from courses.paginations import CoursePagination
from courses.serializers import (CommentSerializers, CourseSerializers, CreatCommentSerializer, CategoryTreeSerializers,
                                 CategoryNodeSerializer, UpdateCommentSerializer)
from courses.models import CourseCategory, Course, Comment
from courses.filters import CourseFilter


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = CourseCategory.objects.is_publish().select_related("icon")
    lookup_field = 'slug'

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return CategoryTreeSerializers
            case 'retrieve':
                return CategoryNodeSerializer
            case _:
                raise NotAcceptable()


class CourseViewSet(ReadOnlyModelViewSet):
    serializer_class = CourseSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['name']
    ordering_fields = ['created_at', "updated_at", "sale_number"]
    pagination_class = CoursePagination
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Course.objects.is_active().select_related('professor__professor_image', 'image') \
            .prefetch_related('course_discount', "category") \
            .annotate(
            discount_value=Case(
                When(course_discount__discount_type='درصدی',
                     then=(F('price') * F('course_discount__value') / Value(100))),
                When(course_discount__discount_type='مقدار',
                     then=F('course_discount__value')),
                default=Value(0),
                output_field=DecimalField(),
            ),
            final_price=F('price') - F('discount_value')
        )

        if 'category_slug' in self.kwargs:
            queryset = queryset.filter(category__slug=self.kwargs['category_slug'])

        return queryset


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
        elif self.request.method == 'PUT':
            return UpdateCommentSerializer
        elif self.request.method == 'PATCH':
            return UpdateCommentSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Comment.objects.filter(course__slug=self.kwargs['course_slug']).select_related("user", "course")
