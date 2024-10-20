from rest_framework.serializers import ModelSerializer, IntegerField, ValidationError, Serializer, CharField, \
    SerializerMethodField
from ulid import ULID
from django.db.transaction import atomic
from datetime import datetime

from users.models import User
from courses.models import Course
from orders.models import Cart, CartItem, OrderItem, Order
from professors.models import Professor


class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class SimpleProfessorSerializer(ModelSerializer):
    class Meta:
        model = Professor
        fields = ['get_full_name']


class CourseCartItemSerialize(ModelSerializer):
    """it is shows field of the course"""
    professor = SimpleProfessorSerializer()
    # final_price = DecimalField(max_digits=12, decimal_places=2, read_only=True)
    discount_value = SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', "professor", 'price', "calc_final_price", "discount_value", "show_image_url"]

    def get_discount_value(self, obj):
        return obj.price - obj.calc_final_price


class CartItemSerializer(ModelSerializer):
    """it is used in the address -->  url /cart/id or /cart/id/items"""
    course = CourseCartItemSerialize(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'course', 'quantity', 'item_price']


class AddCartItemSerializer(ModelSerializer):
    """it is used add cart_item into cart"""
    course_id = IntegerField()

    class Meta:
        model = CartItem
        fields = ['course_id', 'id', 'get_course_name', 'item_price', 'quantity']

        extra_kwargs = {
            'quantity': {'read_only': True},
        }

    def save(self, *args, **kwargs):
        course_id = self.validated_data['course_id']
        cart = Cart.objects.get(pk=self.context['cart_id'])
        try:
            cart_item = CartItem.objects.get(course_id=course_id, cart_id=cart.id)
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart.id, course_id=course_id)
        return self.instance

    def validate_course_id(self, data):
        try:
            Course.objects.get(pk=data)
        except Course.DoesNotExist:
            raise ValidationError('دوره مورد نظر یافت نشد')
        return data


class CartSerializer(ModelSerializer):
    cart_item = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'cart_item', 'total_price']


class OrderItemSerializer(ModelSerializer):
    course = CourseCartItemSerialize()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerialize(ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    user = CharField(source="user.mobile_phone")

    class Meta:
        model = Order
        fields = ['id', 'user', 'payment_status', 'created_at', 'order_item', 'order_total_price']


class CreateOrderSerializer(Serializer):
    cart_id = CharField()

    def validate_cart_id(self, data):
        if not Cart.objects.filter(id=data).exists():
            raise ValidationError('سید خرید یافت نشد')
        elif Cart.objects.filter(id=data).count() == 0:
            raise ValidationError('سبد خرید خالی هست')
        return data

    def generate_ulid(self):
        return str(ULID.from_datetime(datetime.now()))

    def validate(self, attr):
        order = Order.objects.filter(user_id=self.context['user_id']).last()
        if order and order.payment_status == "pending":
            raise ValidationError({"message": "شما از قبل یک سفارش رو دارید, "
                                              "ابتدا وضعیت ان را مشخص کنید"})
        return attr

    def save(self, **kwargs):
        with atomic():
            self.cart_id = self.generate_ulid()
            cart_id = self.validated_data['cart_id']
            order = Order.objects.create(user_id=self.context['user_id'])
            cart_item = CartItem.objects.filter(cart_id=cart_id)
            order_item = [
                OrderItem(
                    order=order,
                    course=item.course,
                    quantity=item.quantity,
                )
                for item in cart_item
            ]
            OrderItem.objects.bulk_create(order_item)
            Cart.objects.filter(pk=cart_id).delete()
            return order


class UpdateOrderItemSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CompleteOrderSerialize(ModelSerializer):
    user = CharField(source='user.mobile_phone')
    order_item = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', "user", "payment_status", "order_item", "order_total_price", "order_number"]
