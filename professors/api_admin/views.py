from rest_framework.viewsets import ModelViewSet

from users.api_admin.pagination import UserAdminPagination
from users.api_admin.permissions import IsAdmin
from .serializers import AdminProfessorSerializer
from ..models import Professor


class AdminProfessorViewSet(ModelViewSet):
    queryset = Professor.objects.select_related('certificate', "professor_image")
    serializer_class = AdminProfessorSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination
