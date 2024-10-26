from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from core.models import CreateMixin, UpdateMixin
from professors.validators import NationCodeValidator
from users.validators import MobileValidator


# Create your models here.


class Professor(CreateMixin, UpdateMixin):
    first_name = models.CharField(_("نام"), max_length=255)
    last_name = models.CharField(_("نام خانوادگی"), max_length=255)
    # professor_contact = models.ForeignKey("ProfessorContact", on_delete=models.PROTECT, related_name="contact",
    #                                       verbose_name=_("راه ارتباطی استاد"))
    nation_code = models.CharField(_("کد ملی"), max_length=11, unique=True,
                                   validators=[NationCodeValidator()])
    birth_date = models.DateField(_("تاریخ تولد"), blank=True, null=True)
    certificate = models.ForeignKey("images.Image", on_delete=models.PROTECT, related_name='certificate_image',
                                    blank=True, null=True, verbose_name=_("عکس اخرین مدرک تحصیلی"))
    professor_image = models.ForeignKey("images.Image", on_delete=models.PROTECT, related_name="professor_image",
                                        verbose_name=_("عکس استاد"))
    field_of_study = models.CharField(_("رشته تحصیلی"), max_length=255)
    name_of_education = models.CharField(_("نام دانشگاه"), max_length=255)

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
    is_active = models.BooleanField(default=False)
    email = models.EmailField(_("ایمیل"), blank=True, null=True)
    mobile_phone = ArrayField(models.CharField(_('شماره تلفن های استاد'), max_length=11),
                              blank=True, null=True, size=5)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'professors'
        verbose_name = _("professor")
        verbose_name_plural = _("professors")
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_professor_email'),
            models.UniqueConstraint(fields=['mobile_phone'], name='unique_professor_mobile_phone')
        ]
