from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from users.api_admin.pagination import UserAdminPagination
from .serializers import AdminCategorySerializer, AdminCourseSerializer, AdminCommentSerializer, \
    AdminDiscountCourseSerializer
from ..models import Course, DiscountCourse, CourseCategory, Comment


class AdminCategoryViewSet(ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = AdminCategorySerializer
    permission_classes = [IsAdminUser]
    pagination_class = UserAdminPagination


class AdminCourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('professor', "image").prefetch_related('category')
    serializer_class = AdminCourseSerializer
    permission_classes = [IsAdminUser]
    pagination_class = UserAdminPagination


class AdminDiscountCourseViewSet(ModelViewSet):
    queryset = DiscountCourse.objects.select_related('course')
    serializer_class = AdminDiscountCourseSerializer
    permission_classes = [IsAdminUser]
    pagination_class = UserAdminPagination


class AdminCommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related("user", "course")
    serializer_class = AdminCommentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = UserAdminPagination
