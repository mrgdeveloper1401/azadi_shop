from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView


from .pagination import OrdersPageNumberPagination
from .serializers import OrderSerializer, CreateOrderSerializer
from .models import Order


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.filter(payment_status='pending').select_related('user').prefetch_related('course')
    serializer_class = OrderSerializer
    pagination_class = OrdersPageNumberPagination

    def get_permissions(self):
        if self.action in ['PUT', "PATCH"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        return {'request': self.request}


class UserOrderAPIView(ListAPIView, RetrieveAPIView):
    serializer_class = OrderSerializer
    pagination_class = OrdersPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return (Order.objects.filter(Q(payment_status='failed') | Q(payment_status="complete"), user=user)
                .select_related('user')
                .prefetch_related('course'))
