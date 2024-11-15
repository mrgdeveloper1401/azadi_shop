from rest_framework.viewsets import ModelViewSet

from users.api_admin.pagination import UserAdminPagination
from users.api_admin.permissions import IsAdmin
from .serializers import AdminCategoryBlogSerializer, AdminPostBlogSerializer
from ..models import CategoryNode, Post


class AdminCategoryBlogViewSet(ModelViewSet):
    queryset = CategoryNode.objects.all()
    serializer_class = AdminCategoryBlogSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination


class AdminPostBlogViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author').prefetch_related('category')
    serializer_class = AdminPostBlogSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination
