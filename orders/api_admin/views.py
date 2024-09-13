from rest_framework.viewsets import ModelViewSet

from orders.api_admin.serializers import AdminCartSerializer
from orders.models import Cart, CartItem, Order, OrderItem
from orders.api_admin.permissions import IsAdmin


class AdminCartViewSet(ModelViewSet):
    queryset = Cart.objects.select_related("user")
    serializer_class = AdminCartSerializer
    permission_classes = [IsAdmin]
