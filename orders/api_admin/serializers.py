from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField

from orders.models import Order, OrderItem
from users.models import User


class AdminOrderSerializer(ModelSerializer):
    user = CharField()

    class Meta:
        model = Order
        fields = '__all__'


class AdminOrderItemSerializer(ModelSerializer):
    course = CharField()

    class Meta:
        model = OrderItem
        fields = '__all__'
