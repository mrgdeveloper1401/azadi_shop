from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet


from users.api_admin.pagination import UserAdminPagination
from users.api_admin.permissions import IsAdmin
from .serializers import AdminPaymentSerializer, Payment


class AdminPaymentViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = AdminPaymentSerializer
    pagination_class = UserAdminPagination
    permission_classes = [IsAdmin]
