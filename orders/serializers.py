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
        extra_kwargs = {
            "user": {'read_only': True},
        }

    def validate_user(self, data):
        user_id = self.context['request'].user.id
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError({"message": _("چنین کاربری وجود ندارد")})
        return data

    def validate(self, attrs):
        course = attrs['course']
        courses = [i.id for i in course]
        valid_course = Course.objects.filter(id__in=courses, is_active=True)
        attrs['valid_course'] = valid_course
        return attrs

    def create(self, validated_data):
        with atomic():
            total_price = sum(i.calc_final_price for i in validated_data['valid_course'])
            course_ids = [i.id for i in validated_data['valid_course']]
            user = self.context['request'].user
            order = Order.objects.create(user=user, total_price=total_price)
            order.course.set(course_ids)
            return order
