from string import digits
from random import choices
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager, OtpManager
from users.validators import MobileValidator
from core.models import CreateMixin, UpdateMixin
from core.datetime_config import after_two_minute
from django.utils.timezone import now


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, CreateMixin, UpdateMixin):
    mobile_phone = models.CharField(_("شماره همراه"), max_length=11, unique=True,
                                    validators=[MobileValidator()])
    is_verified = models.BooleanField(_('احراز هویت'), default=False)
    is_active = models.BooleanField(
        _("فعال"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("دسترسی کارمندی"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    USERNAME_FIELD = 'mobile_phone'

    objects = UserManager()

    def __str__(self):
        return self.mobile_phone

    class Meta:
        db_table = 'user'
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربر ها")


class Grade(models.Model):
    grade_name = models.CharField(_("نام پایه"), max_length=20)

    def __str__(self):
        return self.grade_name

    class Meta:
        db_table = 'grade'
        verbose_name = _("پایه")
        verbose_name_plural = _("پایه")


class Major(models.Model):
    major_name = models.CharField(_("رشته"), max_length=20, unique=True)

    def __str__(self):
        return self.major_name

    class Meta:
        db_table = 'major'
        verbose_name = _("رشته")
        verbose_name_plural = _("رشته ها")


class UserInfo(CreateMixin, UpdateMixin):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='user_info',
                                verbose_name=_("کاربر"))
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='grade',
                              verbose_name=_("پایه"), blank=True, null=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT, related_name='major',
                              verbose_name=_("رشته"), blank=True, null=True)
    gpa = models.FloatField(_("معدل"), validators=[MinValueValidator(0), MaxValueValidator(20)],
                            blank=True, null=True)
    email = models.EmailField(_("ایمیل"), blank=True, null=True)
    first_name = models.CharField(_("نام"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("نام خوانوادگی"), max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = _("پروفایل کاربر")
        verbose_name_plural = _("پروفایل کاربرها")
        db_table = 'user_info'
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]

    def __str__(self):
        return self.user.mobile_phone

    @property
    def get_active(self):
        return self.user.is_active

    @property
    def get_is_verified(self):
        return self.user.is_verified

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class GradeGpa(CreateMixin, UpdateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_grade_gpas',
                             verbose_name=_("کاربر"))
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='grade_gpa',
                              verbose_name=_("پایه"))
    gpa = models.FloatField(_("معدل"), validators=[MinValueValidator(0), MaxValueValidator(20)])

    class Meta:
        db_table = 'grade_gpa'
        verbose_name = _("نمره کاربر")
        verbose_name_plural = _("نمرات کاربر")
        ordering = ('-created_at',)


class Otp(CreateMixin):
    mobile_phone = models.CharField(_("شماره همراه"), max_length=11, validators=[MobileValidator()])
    code = models.PositiveIntegerField(_('کد'), blank=True, null=True)
    expired_at = models.DateTimeField(_('زمان انتقضای کد'), blank=True, null=True)

    objects = OtpManager()

    def __str__(self):
        return self.mobile_phone

    def is_expired(self):
        return now() > self.expired_at

    def delete_if_expired(self):
        if self.is_expired():
            self.delete()
            return True
        return False

    @property
    def generate_random_code(self):
        code = ''.join(choices(digits, k=6))
        return code

    def save(self, *args, **kwargs):
        self.expired_at = after_two_minute()
        self.code = self.generate_random_code
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'otp'
        verbose_name = _('کد')
        verbose_name_plural = _('کدها')
