from courses.models import CourseCategory, Course, DiscountCourse, Comment
from courses.serializers import CourseSerializers, CourseDiscountSerializers, CategorySerializers, CommentSerializers
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .filters import CourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import CoursePaginations
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthenticatedOrAdmin


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializers

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]


class CategoryUpdateRetreveDestoryApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializers
    queryset = CourseCategory.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]


class CourseListAPIView(generics.ListCreateAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.select_related('user', 'category').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['name', 'desc']
    ordering_fields = ['course_discount', 'updated_at', 'created_at']
    pagination_class = CoursePaginations

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]


class CourseUpdateRetreveDestoryApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.select_related('user', 'category').all()
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]


class DiscountCourseApiView(generics.ListCreateAPIView,
                            generics.GenericAPIView):
    queryset = DiscountCourse.objects.select_related('course').all()
    serializer_class = CourseDiscountSerializers
    permission_classes = [IsAdminUser]


class DiscountUpdateApiView(generics.RetrieveUpdateDestroyAPIView,
                            generics.GenericAPIView):
    queryset = DiscountCourse.objects.select_related('course').all()
    serializer_class = CourseDiscountSerializers
    permission_classes = [IsAdminUser]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('user', 'course').all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticatedOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)