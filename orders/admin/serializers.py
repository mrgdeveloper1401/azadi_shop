from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField

from orders.models import Cart, CartItem, Order, OrderItem
from users.models import UserAccount


class AdminCartSerializer(ModelSerializer):
    mobile_phone = CharField(source="user.mobile_phone", read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

        extra_kwargs = {
            "created_at": {"format": "%Y-%m-%d %H:%M:%S"},
        }

    def validate(self, attrs):
        if Cart.objects.filter(user=attrs["user"]).exists():
            raise ValidationError({"message": "cart already exists"})
        return attrs