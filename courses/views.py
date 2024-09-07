from .models import CourseCategory, Course
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .filters import CourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import CoursePaginations
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthenticatedOrAdmin


class CategoryListAPIView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializers


class CourseListAPIView(generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.select_related('user', 'category').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['name', 'desc']
    ordering_fields = ['course_discount', 'updated_at', 'created_at']
    pagination_class = CoursePaginations


class DiscountCourseApiView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = DiscountCourse.objects.select_related('course').all()
    serializer_class = CourseDiscountSerializers
    permission_classes = [AllowAny]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('user', 'course').all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticatedOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
