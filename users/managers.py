from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def _create_user(self, mobile_phone, password, email=None, **extra_fields):
        if not mobile_phone:
            raise ValueError('Mobile phone is required')
        email = self.normalize_email(email)
        user = self.model(mobile_phone=mobile_phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile_phone, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(mobile_phone, password, email, **extra_fields)

    def create_superuser(self, mobile_phone, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(mobile_phone, password, email, **extra_fields)


class OtpManager(Manager):
    def delete_otp(self):
        return self.filter(expired_at__lt=now()).delete()