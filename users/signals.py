from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserAccount, UserInfo, Otp
from users.random_code import generate_random_code
from django.utils.timezone import now, timedelta


@receiver(post_save, sender=UserAccount)
def create_user_related_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)
        Otp.objects.create(user=instance, code=generate_random_code(), expired_at=now() + timedelta(minutes=2))
