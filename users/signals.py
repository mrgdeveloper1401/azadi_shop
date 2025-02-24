from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken

from shop.utils import send_sms
from users.models import User, UserInfo, Otp


@receiver(post_save, sender=User)
def create_user_related_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.get_or_create(user=instance)


@receiver(post_save, sender=Otp)
async def send_otp_sms(sender, created, instance, **kwargs):
    if created:
        await send_sms(instance.mobile_phone, instance.code)
