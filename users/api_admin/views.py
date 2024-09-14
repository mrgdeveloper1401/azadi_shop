from rest_framework.viewsets import ModelViewSet

from users.api_admin.serializers import AdminUserSerializer, AdminOtpSerializer, AdminUserCreateSerializer, \
    AdminUserInfoSerializer
from users.models import UserAccount, UserInfo, Otp
from users.api_admin.permissions import IsAdmin


class AdminUserCreateViewSet(ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return AdminUserCreateSerializer
        else:
            return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        q = self.get_object()
        q.delete()
        return super().destroy(request, *args, **kwargs)


class AdminOtpViewSet(ModelViewSet):
    queryset = Otp.objects.all()
    serializer_class = AdminOtpSerializer
    permission_classes = [IsAdmin]


class AdminUserInfoViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = AdminUserInfoSerializer
    permission_classes = [IsAdmin]
