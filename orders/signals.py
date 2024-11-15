from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from payments.models import Payment
from shop.utils import create_token


@receiver(post_save, sender=Order)
def create_cart(sender, instance, created, **kwargs):
    if instance.payment_status == 'complete':
        payment = [
            Payment(
                user=item.user,
                course=item.course,
                final_price=item.course.calc_final_price,
                license_key=create_token(item.user.mobile_phone, item.course, item.user.user_info.get_full_name)
            )
            for item in instance
        ]
        Payment.objects.bulk_create(payment)
