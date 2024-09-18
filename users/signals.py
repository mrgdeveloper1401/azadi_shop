from django.db.models.signals import post_save
from django.dispatch import receiver
from core.datetime_config import after_two_minute

from users.models import UserAccount, UserInfo, Otp
from users.random_code import generate_random_code


@receiver(post_save, sender=UserAccount)
def create_user_related_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
        Otp.objects.create(user=instance, code=generate_random_code(), expired_at=after_two_minute)
