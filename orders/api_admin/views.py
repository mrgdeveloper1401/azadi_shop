from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin

from orders.api_admin.serializers import AdminOrderSerializer, AdminOrderItemSerializer
from orders.models import Order, OrderItem
from orders.api_admin.permissions import IsAdmin
from users.api_admin.pagination import UserAdminPagination


class AdminOrderViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Order.objects.select_related("user")
    serializer_class = AdminOrderSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserAdminPagination


class AdminOrderItemViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = OrderItem.objects.select_related('course')
    serializer_class = AdminOrderItemSerializer
    pagination_class = UserAdminPagination
    permission_classes = [IsAdmin]
