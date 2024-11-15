from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.utils import send_sms
from users.models import User, UserInfo, Otp
from users.tasks import send_otp_code


@receiver(post_save, sender=User)
def create_user_related_info(sender, instance, created, **kwargs):
    # if not instance.is_superuser:
    #     Otp.objects.get_or_create(mobile_phone=instance.mobile_phone)
    if instance.is_verified:
        UserInfo.objects.get_or_create(user=instance)


@receiver(post_save, sender=Otp)
def send_otp_sms(sender, created, instance, **kwargs):
    if created:
        # send_otp_code.delay(instance.mobile_phone, instance.code)
        send_sms(instance.mobile_phone, instance.code)
