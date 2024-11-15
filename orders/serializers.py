from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _

from courses.models import Course
from users.models import User
from .models import Order


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', "course"]

    def validate_user(self, data):
        try:
            user = User.objects.get(pk=data.id)
        except User.DoesNotExist:
            raise ValidationError({"message": _("چنین کاربری وجود ندارد")})
        else:
            order = Order.objects.filter(user=user).last()
            if order and order.payment_status == 'pending':
                raise ValidationError({"message": _("شما از قبل یه سفارش دارید لطفا وضعیت ان را مشخص کنید")})
        return data

    def validate(self, attrs):
        course = attrs['course']
        c = [i.id for i in course]
        valid_course = Course.objects.filter(id__in=c, is_active=True)
        attrs['valid_course'] = valid_course
        return attrs

    def create(self, validated_data):
        with atomic():
            total_price = sum(i.calc_final_price for i in validated_data['valid_course'])
            course_ids = [i.id for i in validated_data['valid_course']]
            user = validated_data['user']
            order = Order.objects.create(user=user, total_price=total_price)
            order.course.set(course_ids)
            return order
