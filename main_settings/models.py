from django.contrib.gis.db.models import PointField
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin
from users.validators import MobileValidator


# Create your models here.


class HeaderSite(CreateMixin, UpdateMixin):
    title = models.CharField(_("title"), max_length=50)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'header_site'
        verbose_name = _("هدر سایت")
        verbose_name_plural = _("هدر سایت")


class HomeSite(CreateMixin, UpdateMixin):
    site_logo = models.ForeignKey("images.Image", on_delete=models.PROTECT, related_name='home_site_logo',
                                  verbose_name=_("عکس لوگو سایت"))
    slider_image = models.ManyToManyField("images.Image", related_name='home_site_slider',
                                          verbose_name=_("عکس اسلایدر سایت"))
    header_phone_number = models.CharField(_("شماره تماس"), max_length=15, unique=True)
    about_us_body = models.TextField(_("متن درباره ما"))
    about_us_image = models.ForeignKey("images.Image", on_delete=models.PROTECT,
                                       related_name='home_site_about_us_image')
    slider_professor_image = models.ForeignKey('images.Image', related_name='home_site_slider_professor_image',
                                               verbose_name=_("عکس اساتید"), on_delete=models.PROTECT)
    email = models.EmailField(_("ایمیل"), unique=True)
    description_footer = models.TextField(_("توضیح فوتر"))
    awards_image = models.ManyToManyField('images.Image', related_name='home_site_awards_image',
                                          verbose_name=_('عکس جوایز و افتخارات'))
    team_image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='home_site_team_image',
                                   verbose_name=_("عکس تیم"))
    is_active = models.BooleanField(_("فعال باشد"), default=True)

    def __str__(self):
        return f"{self.header_phone_number} {self.email} {self.is_active}"

    class Meta:
        db_table = 'home_site'
        verbose_name = _("بخش هایی از سایت")
        verbose_name_plural = _("بخش های از سایت")


class Services(CreateMixin, UpdateMixin):
    title = models.CharField(_("عنوان خدمات ما"), max_length=100, unique=True)
    services_image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='services_image',
                                       verbose_name=_("عکس یا لوگوی خدمات ما"))
    description = models.TextField(_("توضیحات خدمات ما "), blank=True, null=True)
    link = models.URLField(_("ادرس"))
    is_active = models.BooleanField(_("قعال باشد"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'services'
        verbose_name = _("خدمات")
        verbose_name_plural = _("خدمات")


class ContactUs(CreateMixin, UpdateMixin):
    full_name = models.CharField(_("نام و نام خوانوادگی"), max_length=150)
    mobile_phone = models.CharField(_("شماره موبایل"), max_length=11, validators=[MobileValidator()])
    description = models.TextField(_("توضیح"))

    def __str__(self):
        return f'{self.full_name} {self.mobile_phone}'

    class Meta:
        db_table = 'contact_us'
        verbose_name = _("ارتباط با ما")
        verbose_name_plural = _("ارتباط با ما")


class TopRankProfessor(CreateMixin, UpdateMixin):
    full_name = models.CharField(_("نام و نام خوانوادگی"), max_length=50)
    field_title = models.CharField(_("عنوان درس"), max_length=50)
    professor_image = models.ForeignKey('images.Image', on_delete=models.PROTECT,
                                        related_name='top_rank_professor_image', verbose_name=_("عکس استاد"))

    def __str__(self):
        return f"{self.full_name} {self.field_title}"

    class Meta:
        db_table = 'top_rank_professo r'
        verbose_name = _("برترین اساتید")
        verbose_name_plural = _("برترین اساتید")


class TopRankStudent(CreateMixin, UpdateMixin):
    # slug = models.SlugField(_("slug"), unique=True, allow_unicode=True)
    first_name = models.CharField(_("نام"), max_length=150)
    last_name = models.CharField(_("نام خوانوادگی"), max_length=150)
    fields = models.CharField(_("عنوان شغلی"), max_length=50)
    is_active = models.BooleanField(_("فعال بودن"), default=True)

    class TitleChoices(models.TextChoices):
        experimental = 'experimental', _("تجربی")
        math = 'math', _("ریاضی")
        human = 'human', _("انسانی")

    title = models.CharField(_("title"), max_length=12, choices=TitleChoices.choices)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    class Meta:
        db_table = 'top_rank'
        verbose_name = _("برترین دانشجویان")
        verbose_name_plural = _("برترین دانشجویان")


class Newsletter(CreateMixin, UpdateMixin):
    email = models.EmailField(_("email"))

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'newsletter'
        verbose_name = _("خبرنامه")
        verbose_name_plural = _("خبرنامه")


class BusinessAddress(CreateMixin, UpdateMixin):
    address = models.TextField(_("ادرس"))
    location = PointField(verbose_name=_("لوکیشن"), geography=True)
    is_active = models.BooleanField(_("فعال بودن"), default=True)

    def __str__(self):
        return f'{self.address[:20]} {self.is_active}'

    class Meta:
        db_table = 'business_address'
        verbose_name = _("ادرس شعب")
        verbose_name_plural = _("ادرس شعب ها")
