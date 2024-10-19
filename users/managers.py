from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager

from core.datetime_config import after_two_minute
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, mobile_phone, password, **extra_fields):
        if not mobile_phone:
            raise ValueError('لطفا شماره همراه خود را وارد نمایید')
        user = self.model(mobile_phone=mobile_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_verified", True)
        return self.create_user(mobile_phone, password, **extra_fields)


class OtpManager(Manager):
    def delete_otp(self):
        return self.filter(expired_at__lt=now()).delete()
