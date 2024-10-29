from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from users.api_admin.pagination import UserAdminPagination
from users.api_admin.serializers import AdminUserSerializer, AdminOtpSerializer, AdminUserCreateSerializer, \
    AdminUserInfoSerializer, MajorSerializer, GradeGpaSerializer, GradeSerializer
from users.models import User, UserInfo, Otp, Grade, Major, GradeGpa
from users.api_admin.permissions import IsAdmin
from rest_framework.permissions import AllowAny


class AdminUserCreateViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return AdminUserCreateSerializer
        else:
            return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        q = self.get_object()
        if q.is_deleted:
            return Response({"message": "you have already deleted account"})
        q.delete()
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method in 'POST':
            return [AllowAny()]
        return super().get_permissions()


class AdminOtpViewSet(ModelViewSet):
    queryset = Otp.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = AdminOtpSerializer
    pagination_class = UserAdminPagination


class AdminUserInfoViewSet(ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = UserInfo.objects.select_related("user", "grade", "major")
    serializer_class = AdminUserInfoSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class GradeGpaViewSet(ModelViewSet):
    queryset = GradeGpa.objects.select_related('grade', "user")
    serializer_class = GradeGpaSerializer


class MajorViewSet(ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
