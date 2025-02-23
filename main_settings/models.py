from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin, SoftDeleteMixin
from shop.utils import image_upload_validator
from users.validators import MobileValidator


# Create your models here.
class HeaderSite(CreateMixin, UpdateMixin, SoftDeleteMixin):
    title = models.CharField(_("title"), max_length=50)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'header_site'
        verbose_name = _("هدر سایت")
        verbose_name_plural = _("هدر سایت")


class HomeSite(CreateMixin, UpdateMixin, SoftDeleteMixin):
    site_logo = models.ImageField(_('عکس لوگو سایت'), upload_to='main_settings/header_logo/')
    footer_logo = models.ImageField(_('عکس لوگو فوتر سایت'), upload_to='main_settings/footer_logo/', null=True)
    home_hero_section_image = models.ImageField(upload_to="main_settings/home_hero_section_image/",
                                                validators=[image_upload_validator], null=True)
    home_hero_section_title = models.CharField(max_length=50)
    home_hero_section_description = models.CharField(max_length=500)
    home_about_section_title = models.CharField(max_length=50)
    home_about_section_body = models.CharField(max_length=500)
    home_about_section_banner = models.ImageField(upload_to="main_settings/home_about_section_banner/",
                                                  validators=[image_upload_validator], null=True)
    home_middle_page_banner = models.ImageField(upload_to="main_settings/home_middle_page_banner/",
                                                validators=[image_upload_validator], null=True)
    office_contact_number = ArrayField(models.CharField(max_length=15))
    office_email = ArrayField(models.EmailField())
    description_of_our_group = models.CharField(max_length=600)
    is_main_settings = models.BooleanField(default=True)

    class Meta:
        db_table = 'home_site'
        verbose_name = _("صفحه اصلی")
        verbose_name_plural = _("صفحه اصلی")


class ContactUs(CreateMixin, UpdateMixin, SoftDeleteMixin):
    full_name = models.CharField(_("نام و نام خوانوادگی"), max_length=150)
    mobile_phone = models.CharField(_("شماره موبایل"), max_length=11, validators=[MobileValidator()])
    description = models.TextField(_("توضیح"))

    def __str__(self):
        return f'{self.full_name} {self.mobile_phone}'

    class Meta:
        db_table = 'contact_us'
        verbose_name = _("تماس با ما")
        verbose_name_plural = _("تماس با ما")


class ContactUsSocial(CreateMixin, UpdateMixin, SoftDeleteMixin):
    social_name = models.CharField(max_length=50, null=True, help_text=_("نام شکبه اجتماعی"))
    social_link = models.CharField(max_length=50, help_text=_("ادرس شبکه اجتماعی"))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.social_link

    class Meta:
        db_table = 'social'
        verbose_name = _("شبکه اجتماعی")
        verbose_name_plural = _("شبکه های اجتماعی")


class TopRankProfessor(CreateMixin, UpdateMixin):
    full_name = models.CharField(_("نام و نام خوانوادگی"), max_length=50)
    field_title = models.CharField(_("عنوان درس"), max_length=50)
    professor_image = models.ImageField(_("عکس اساتید"), upload_to='main_settings/top_professor/%Y/%m/%d')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    @property
    def professor_image_url(self):
        return self.professor_image.url

    class Meta:
        db_table = 'top_rank_professor'
        verbose_name = _("برترین اساتید")
        verbose_name_plural = _("برترین اساتید")


class Newsletter(CreateMixin, UpdateMixin):
    email = models.EmailField(_("email"))

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'newsletter'
        verbose_name = _("خبرنامه")
        verbose_name_plural = _("خبرنامه")


class BusinessAddress(CreateMixin, UpdateMixin):
    location_lat = models.DecimalField(max_digits=20, decimal_places=10)
    location_long = models.DecimalField(max_digits=20, decimal_places=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.location_lat} {self.location_long}'

    class Meta:
        db_table = 'business_address'
        verbose_name = _("ادرس شعب")
        verbose_name_plural = _("ادرس شعب ها")
