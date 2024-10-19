from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, UserInfo, Otp


@receiver(post_save, sender=User)
def create_user_related_info(sender, instance, created, **kwargs):
    if not instance.is_superuser:
        Otp.objects.get_or_create(mobile_phone=instance.mobile_phone)
    if instance.is_verified:
        UserInfo.objects.get_or_create(user=instance)
