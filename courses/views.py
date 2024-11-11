from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.db.models import Case, When, F, DecimalField, Value, DateTimeField

from courses.permissions import IsOwner
from courses.paginations import CoursePagination
from courses.serializers import CommentSerializers, CourseSerializers, CreatCommentSerializer, UpdateCommentSerializer, \
    CategorySerializers, DiscountCourseSerializer
from courses.models import CourseCategory, Course, Comment, DiscountCourse
from courses.filters import CourseFilter
from users.permissions import IsVerifiedUser


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializers


class CourseViewSet(ReadOnlyModelViewSet):
    serializer_class = CourseSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['name']
    ordering_fields = ['created_at', "updated_at", "sale_number"]
    pagination_class = CoursePagination

    def get_queryset(self):
        queryset = Course.objects.is_active().select_related('professor') \
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
            final_price=F("price") - F("discount_value"),
            amount=F("course_discount__value"),
            discount_time=Case(
                When(course_discount__is_active=True, then=F("course_discount__expired_date")),
                default=Value(None), output_field=DateTimeField()
            )
        )

        if 'category_pk' in self.kwargs:
            queryset = queryset.filter(category__pk=self.kwargs['category_pk'])

        return queryset


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = [IsOwner, IsVerifiedUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"course_pk": self.kwargs['course_pk'], "request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatCommentSerializer
        elif self.request.method == 'PUT':
            return UpdateCommentSerializer
        elif self.request.method == 'PATCH':
            return UpdateCommentSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Comment.objects.filter(course__pk=self.kwargs['course_pk']).select_related("user", "course")


class DiscountViewSet(ReadOnlyModelViewSet):
    queryset = DiscountCourse.objects.filter(is_active=True, expired_date__gt=now()).select_related('course',
                                                                                                    "course__professor")
    serializer_class = DiscountCourseSerializer
