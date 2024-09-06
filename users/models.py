from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta

from users.managers import UserManager, OtpManager
from users.validators import MobileValidator
from users.random_code import generate_random_code


# Create your models here.
class UserAccount(AbstractUser):
    is_verified = models.BooleanField(default=False)
    mobile_phone = models.CharField(_("mobile phone"), max_length=15, unique=True,
                                    validators=[MobileValidator()])
    username = None

    USERNAME_FIELD = 'mobile_phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = UserManager()

    class Meta:
        db_table = 'user'
        ordering = ("-date_joined",)

    def __str__(self):
        return self.mobile_phone


class UserInfo(models.Model):
    GRADE_CHOICES = (
        ('دهم', 'دهم'),
        ('یازدهم', 'یازدهم'),
        ('دوازدهم', 'دوازدهم')

    )
    MAJOR_CHOICES = (
        ('تجربی', 'تجربی'),
        ('ریاضی', 'ریاضی'),
        ('انسانی', 'انسانی')

    )
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='user_info')
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default='دهم')
    major = models.CharField(max_length=10, choices=MAJOR_CHOICES, default='تجربی')

    class Meta:
        db_table = 'user_info'

    def __str__(self):
        return self.user.mobile_phone

    @property
    def get_active(self):
        return self.user.is_active


class Otp(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_otp')
    code = models.PositiveSmallIntegerField(_('OTP code'), unique=True, default=generate_random_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=now() + timedelta(minutes=2))

    objects = OtpManager()

    class Meta:
        db_table = 'opt'
        verbose_name = _('otp')
        verbose_name_plural = _('OTPs')

    def __str__(self):
        return self.user.mobile_phone

    def is_expired(self):
        return now() > self.expired_at

    def delete_if_expired(self):
        if self.is_expired():
            self.delete()
            return True
        return False

