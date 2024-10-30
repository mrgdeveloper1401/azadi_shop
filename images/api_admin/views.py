from rest_framework.viewsets import ModelViewSet

from orders.api_admin.permissions import IsAdmin
from users.api_admin.pagination import UserAdminPagination
from ..models import Image
from .serializers import AdminImageSerializer


class AdminImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = AdminImageSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination
