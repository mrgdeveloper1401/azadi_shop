from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from core.models import CreateMixin, UpdateMixin
from professors.validators import NationCodeValidator, validate_birth_date


# Create your models here.
class Professor(CreateMixin, UpdateMixin):
    first_name = models.CharField(_("نام"), max_length=50)
    last_name = models.CharField(_("نام خانوادگی"), max_length=50)
    nation_code = models.CharField(_("کد ملی"), max_length=11, unique=True,
                                   validators=[NationCodeValidator()])
    birth_date = models.DateField(_("تاریخ تولد"), validators=[validate_birth_date],
                                  help_text=_("%YYYY-%mm-%dd به این شکل میتوانید وارد کنید"))
    certificate = models.ImageField(_("عکس مدرک تحصیلی استاد"), upload_to="professor/certificate/%Y/%m/%d", blank=True,
                                    null=True)
    professor_image = models.ImageField(_("عکس استاد"), upload_to='professor/image/%Y/%m/%d')
    field_of_study = models.CharField(_("رشته تحصیلی"), max_length=100)
    name_of_education = models.CharField(_("نام دانشگاه"), max_length=50)

    class EducationStatus(models.TextChoices):
        diploma = 'دیپلم', _("دیپلم")
        associate_graduate = 'فارغ التحصیل کاردانی', _('فارغ التحصیل کاردانی')
        undergraduate_student = 'دانشجوی کارشناسی', _("دانشجوی کارشناسی")
        bachelors_student = 'فارغ التحصیل کارشناسی', _('فارغ التحصیل کارشناسی')
        master_student = 'دانشجوی کارشناسی ارشد', _("دانشجوی کارشناسی ارشد")
        master_degree_graduate = 'فارغ التحصیل کارشناسی ارشد', _("فارغ التحصیل کارشناسی ارشد")
        doctoral_student = 'دانشجوی دکترا', _("دانشجوی دکترا")
        phd_graduate = 'فارغ التحصیل دکترا', _("فارغ التحصیل دکترا")
    education_status = models.CharField(_("وضعیت تحصیل"), choices=EducationStatus.choices, max_length=26)
    is_active = models.BooleanField(_('فعال'), default=True)
    email = models.EmailField(_("ایمیل"), blank=True, null=True)
    mobile_phone = ArrayField(models.CharField(_('شماره تلفن های استاد'), max_length=11),
                              blank=True, null=True, size=5,
                              help_text=_("اگر استاد چندین شماره موبایل رو دارد با کاما از هم جدا کنید"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'professors'
        verbose_name = _("استاد")
        verbose_name_plural = _("استاید ها")
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_professor_email', condition=Q(email__isnull=True)),
            models.UniqueConstraint(fields=['mobile_phone'], name='unique_professor_mobile_phone',
                                    condition=Q(mobile_phone__isnull=True))
        ]
