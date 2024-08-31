from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserAccount, UserInfo, Otp
from users.random_code import generate_random_code
from django.utils.timezone import now, timedelta


@receiver(post_save, sender=UserAccount)
def create_userinfo(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)


@receiver(post_save, sender=UserAccount)
def create_otp_code(sender, instance, created, **kwargs):
    if created:
        Otp.objects.create(user=instance,
                           code=generate_random_code(),
                           expired_at=now() + timedelta(minutes=2))


@receiver(post_save, sender=Otp)
def delete_expired_otp(sender, created, instance, **kwargs):
    if created:
        if instance.expired_at and now() > instance.expired_at:
            instance.delete()
