from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin
from django_jalali.db.models import jDateField
# Create your models here.


class Professor(CreateMixin, UpdateMixin):
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last_name"), max_length=255)
    email = models.EmailField(_("email"), blank=True, null=True)
    mobile_phone = models.CharField(_("mobile phone"), max_length=15, blank=True, null=True)
    professor_contact = models.ForeignKey("ProfessorContact", on_delete=models.PROTECT, related_name="contact")
    nation_code = models.CharField(_("nation code"), max_length=11, unique=True)
    birth_date = jDateField(_("birth date"), blank=True, null=True)
    certificate = models.ForeignKey("images.Image", on_delete=models.PROTECT, related_name='certificate_image',
                                    blank=True, null=True)
    professor_image = models.ForeignKey("images.Image", on_delete=models.PROTECT, related_name="professor_image")
    field_of_study = models.CharField(_("field of study"), max_length=255)
    name_of_education = models.CharField(_("name of education"), max_length=255)

    class EducationStatus(models.TextChoices):
        diploma = 'دیپلم', _("دیپلم")
        associateـgraduate = 'فارغ التحصیل کاردانی', _('فارغ التحصیل کاردانی')
        undergraduate_student = 'دانشجوی کارشناسی', _("دانشجوی کارشناسی")
        bachelors_student = 'فارغ التحصیل کارشناسی', _('فارغ التحصیل کارشناسی')
        master_student = 'دانشجوی کارشناسی ارشد', _("دانشجوی کارشناسی ارشد")
        master_degree_graduate = 'فارغ التحصیل کارشناسی ارشد', _("فارغ التحصیل کارشناسی ارشد")
        doctoral_student = 'دانشجوی دکترا', _("دانشجوی دکترا")
        phd_graduate = 'فارغ التحصیل دکترا', _("فارغ التحصیل دکترا")
    education_status = models.CharField(_("education status"), choices=EducationStatus.choices, max_length=26)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.education_status}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'professors'
        verbose_name = _("professor")
        verbose_name_plural = _("professors")


class ProfessorContact(CreateMixin, UpdateMixin):
    contact_name = models.CharField(_("contact name"), max_length=100)
    contact_url = models.URLField(_("contact url"), blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.contact_name

    class Meta:
        db_table = 'professor_contact'
        verbose_name = _("professor contact")
        verbose_name_plural = _("professor contacts")
