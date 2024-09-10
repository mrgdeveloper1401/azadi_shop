from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from orders.models import Cart, CartItem, Order
from orders.serializers import CartSerializer, AddCartItemSerializer, CartItemSerializer, OrderSerialize, \
    CreateOrderSerializer, UpdateOrderItemSerializer
from orders.permissions import IsOwner
# Create your views here.


class CartViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('cart_item', 'cart_item__course')
    serializer_class = CartSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(user=user)
        return queryset


class CartItemViewSet(RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = CartItem.objects.select_related('course')
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk'],
                'user': self.request.user}

    def get_queryset(self):
        cart_id = self.kwargs['cart_pk']
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(cart_id=cart_id)
        return queryset


class OrderViewSet(ModelViewSet):
    queryset = (Order.objects.select_related('user').prefetch_related('order_item', 'order_item__course'))

    def create(self, request, *args, **kwargs):
        ser_data = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        ser_data.is_valid(raise_exception=True)
        order = ser_data.save()
        ser_data = OrderSerialize(order)
        return Response(ser_data.data, status=HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return UpdateOrderItemSerializer
        return OrderSerialize

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsOwner()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(user=self.request.user)
        return queryset
