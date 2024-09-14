from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError

from users.managers import UserManager, OtpManager
from users.validators import MobileValidator
from users.random_code import generate_random_code
from core.models import SoftDeleteMixin, CreateMixin, UpdateMixin


# Create your models here.
class UserAccount(AbstractUser, SoftDeleteMixin):
    is_verified = models.BooleanField(default=False)
    mobile_phone = models.CharField(_("mobile phone"), max_length=15, unique=True,
                                    validators=[MobileValidator()])
    username = None
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    USERNAME_FIELD = 'mobile_phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = UserManager()

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.mobile_phone

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.is_verified = False
        self.is_superuser = False
        self.is_staff = False
        self.is_deleted = True
        self.deleted_at = now()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'user'
        ordering = ("-date_joined",)


class UserInfo(CreateMixin, UpdateMixin):
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

    @property
    def get_is_deleted(self):
        return self.user.is_deleted

    @property
    def get_deleted_at(self):
        return self.user.deleted_at

    @property
    def get_is_verified(self):
        return self.user.is_verified

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    def delete(self, *args, **kwargs):
        self.user.is_active = False
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.deleted_at = now()
        self.user.is_deleted = True
        self.user.is_verified = False
        self.user.save()
        return super().save(*args, **kwargs)


class Otp(CreateMixin):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_otp')
    code = models.PositiveIntegerField(_('OTP code'), unique=True, default=generate_random_code)
    expired_at = models.DateTimeField(blank=True, null=True)

    objects = OtpManager()

    def __str__(self):
        return self.user.mobile_phone

    def is_expired(self):
        return now() > self.expired_at

    def delete_if_expired(self):
        if self.is_expired():
            self.delete()
            return True
        return False

    def clean(self):
        otp_code = Otp.objects.filter(user=self.user)
        user_account = UserAccount.objects.get(mobile_phone=self)
        if user_account.is_active and user_account.is_verified:
            raise ValidationError({"user": "user is active and verified"})
        elif user_account.is_deleted:
            raise ValidationError({"user": "user is deleted"})
        elif otp_code.exists():
            raise ValidationError({"user": "otp code already exits"})
        super().clean()

    def save(self, *args, **kwargs):
        self.expired_at = now() + timedelta(minutes=2)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'otp'
        verbose_name = _('otp')
        verbose_name_plural = _('OTPs')


