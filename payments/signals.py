# from django.db.models.signals import post_save
# from django.db.transaction import atomic
# from django.dispatch import receiver
# from django.utils.crypto import get_random_string
#
# from shop.utils import create_token
# from orders.models import Order
# from .models import Payment
#
#
# @receiver(post_save, sender=Order)
# def create_licence(sender, instance, created, **kwargs):
#     with atomic():
#         if instance.payment_status == "complete":
#             course = [i.course.id for i in instance.order_item.all()]
#             license_course = [i.course.course_license for i in instance.order_item.all()]
#             name = instance.user.user_info.get_full_name
#             mobile_phone = instance.user.mobile_phone
#             token = create_token(mobile_phone, license_course, name)
#             Payment.objects.get_or_create(
#                 user=instance.user,
#                 course_id=course[0],
#                 final_price=instance.order_total_price,
#                 order_number=get_random_string(10),
#                 license_key=token['key'],
#             )
