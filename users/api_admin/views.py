from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.api_admin.serializers import AdminUserSerializer, AdminOtpSerializer, AdminUserCreateSerializer, \
    AdminUserInfoSerializer, AdminOtpCreateSerializer
from users.models import UserAccount, UserInfo, Otp
from users.api_admin.permissions import IsAdmin


class AdminUserCreateViewSet(ModelViewSet):
    queryset = UserAccount.objects.prefetch_related("user_permissions", "groups")
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdmin]

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


class AdminOtpViewSet(ModelViewSet):
    queryset = Otp.objects.select_related("user")
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return AdminOtpCreateSerializer
        else:
            return AdminOtpSerializer


class AdminUserInfoViewSet(ModelViewSet):
    queryset = UserInfo.objects.select_related("user")
    serializer_class = AdminUserInfoSerializer
    permission_classes = [IsAdmin]
    
    def destroy(self, request, *args, **kwargs):
        q = self.get_object()
        if q.user.is_deleted:
            return Response({"message": "you have already deleted account"})
        return super().destroy(request, *args, **kwargs)
