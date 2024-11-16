from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from payments.models import Payment
from shop.utils import create_token


@receiver(post_save, sender=Order)
def create_cart(sender, instance, created, **kwargs):
    if instance.payment_status == 'complete':
        for item in instance.course.all():
            token = create_token(mobile_phone=instance.user.mobile_phone, course=item.course_license,
                                 name=instance.user.get_user_info_name)
            Payment.objects.create(
                user=instance.user,
                course=item,
                final_price=item.calc_final_price,
                license_key=token['key']
            )
