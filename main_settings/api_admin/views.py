from rest_framework.viewsets import ModelViewSet

from orders.api_admin.permissions import IsAdmin
from users.api_admin.pagination import UserAdminPagination
from .serializers import (AdminHeaderSiteSerializer, HomeSiteSerializer, AdminContactUsSerializer,
                          AdminTopRankStudentSerializer, AdminTopRankProfessorSerializer, AdminNewsLatterSerializer)
from ..models import HeaderSite, HomeSite, ContactUs, TopRankStudent, TopRankProfessor, Newsletter


class AdminHeaderSiteViewSet(ModelViewSet):
    queryset = HeaderSite.objects.filter(is_active=True)
    serializer_class = AdminHeaderSiteSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination


class HomeSiteViewSet(ModelViewSet):
    queryset = HomeSite.objects.prefetch_related(
        "slider_image", "about_us_image", "slider_professor_image", "awards_image", "team_image"
    ).select_related('site_logo')
    serializer_class = HomeSiteSerializer
    pagination_class = UserAdminPagination
    permission_classes = [IsAdmin]


class AdminContactUsViewSet(ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = AdminContactUsSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination


class AdminTopRankStudentViewSet(ModelViewSet):
    queryset = TopRankStudent.objects.all()
    serializer_class = AdminTopRankStudentSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination


class AdminTopRankProfessorViewSet(ModelViewSet):
    queryset = TopRankProfessor.objects.all()
    serializer_class = AdminTopRankProfessorSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination


class AdminNewsLatterViewSet(ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = AdminNewsLatterSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination
