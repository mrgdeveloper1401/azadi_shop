from rest_framework.viewsets import ModelViewSet

from orders.admin.serializers import AdminCartSerializer
from orders.models import Cart, CartItem, Order, OrderItem
from orders.admin.permissions import IsAdmin


class AdminCartViewSet(ModelViewSet):
    queryset = Cart.objects.select_related("user")
    serializer_class = AdminCartSerializer
    permission_classes = [IsAdmin]
