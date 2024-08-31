from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, mobile_phone, email, password, **extra_fields):
        if not mobile_phone:
            raise ValueError('Mobile phone is required')
        email = self.normalize_email(email)
        user = self.model(mobile_phone=mobile_phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile_phone, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile_phone, email, password, **extra_fields)

    def create_superuser(self, mobile_phone, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(mobile_phone, email, password, **extra_fields)
