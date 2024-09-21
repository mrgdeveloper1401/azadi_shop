from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db.models import PointField

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
        verbose_name = _("header site")
        verbose_name_plural = _("header sites")


class SiteLogo(CreateMixin, UpdateMixin):
    logo = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='site_logo')
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        db_table = 'site_logo'
        verbose_name = _("site logo")
        verbose_name_plural = _("site logos")


class Slider(CreateMixin, UpdateMixin):
    title = models.CharField(_("title"), max_length=100, unique=True)
    slug = models.SlugField(_("slug"), unique=True, allow_unicode=True)
    slider_image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='slider_image')
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'slider'
        verbose_name = _("slider")
        verbose_name_plural = _("sliders")


class AboutUs(CreateMixin, UpdateMixin):
    title = models.CharField(_("title"), max_length=100, unique=True)
    description = models.TextField(_("description"))
    about_us_image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='about_us_image')
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'about_us'
        verbose_name = _("about us")
        verbose_name_plural = _("about us")


class Services(CreateMixin, UpdateMixin):
    title = models.CharField(_("title"), max_length=100, unique=True)
    services_image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='services_image')
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'services'
        verbose_name = _("services")
        verbose_name_plural = _("services")


class ContactUs(CreateMixin, UpdateMixin):
    full_name = models.CharField(_("full name"), max_length=150)
    mobile_phone = models.CharField(_("mobile phone"), max_length=11, validators=[MobileValidator()])
    description = models.TextField(_("description"))

    def __str__(self):
        return f'{self.full_name} {self.mobile_phone}'

    class Meta:
        db_table = 'contact_us'
        verbose_name = _("contact us")
        verbose_name_plural = _("contact us")


class ProfessorImages(CreateMixin, UpdateMixin):
    professor_image = models.ManyToManyField('images.Image', related_name='professor_images')
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return f"{self.id} {self.is_active}"

    class Meta:
        db_table = 'professor_images'
        verbose_name = _("professor images")
        verbose_name_plural = _("professor images")


class TopRank(CreateMixin, UpdateMixin):
    slug = models.SlugField(_("slug"), unique=True, allow_unicode=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    fields = models.CharField(_("fields"), max_length=50)
    is_active = models.BooleanField(_("is active"), default=True)

    class TitleChoices(models.TextChoices):
        experimental = 'experimental', _("تجربی")
        math = 'math', _("ریاضی")
        human = 'human', _("انسانی")
    title = models.CharField(_("title"), max_length=12, choices=TitleChoices.choices)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    class Meta:
        db_table = 'top_rank'
        verbose_name = _("top rank")
        verbose_name_plural = _("top rank")


class Newsletter(CreateMixin, UpdateMixin):
    email = models.EmailField(_("email"))

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'newsletter'
        verbose_name = _("newsletter")
        verbose_name_plural = _("newsletter")


class Footer(CreateMixin, UpdateMixin):
    footer_logo = models.ForeignKey("images.Image", on_delete=models.PROTECT, related_name='footer_logo')
    footer_description = models.TextField(_("footer description"))
    footer_address = models.ManyToManyField("FooterAddress", related_name='footer_address')
    mobile_phone = models.CharField(_("mobile phone"), max_length=11, validators=[MobileValidator()])
    email = models.EmailField(_("email"))
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return f'{self.mobile_phone} {self.email}'

    class Meta:
        db_table = 'footer'
        verbose_name = _("footer")
        verbose_name_plural = _("footer")


class FooterAddress(CreateMixin, UpdateMixin):
    city = models.CharField(_("city"), max_length=150)
    state = models.CharField(_("state"), max_length=150)
    street = models.TextField(_("street"))
    postal_code = models.CharField(_("postal code"), max_length=10, unique=True)
    location = PointField(_("location"))
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return f"{self.state} {self.city} {self.is_active}"

    class Meta:
        db_table = 'footer_address'
        verbose_name = _("footer address")
        verbose_name_plural = _("footer address")


class FooterSocial(CreateMixin, UpdateMixin):
    footer = models.ForeignKey(Footer, on_delete=models.CASCADE, related_name='footer_social')
    social_name = models.CharField(_("social name"), max_length=150)
    social_url = models.URLField(_('footer url'))
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return f"{self.social_name} {self.is_active}"

    class Meta:
        db_table = 'footer_social'
        verbose_name = _("footer social")
        verbose_name_plural = _("footer social")


class Awards(CreateMixin, UpdateMixin):
    awards_title = models.CharField(_("awards title"), max_length=100)
    awards_image = models.ManyToManyField('images.Image', related_name='awards_image')
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return f"{self.awards_title} {self.is_active}"

    class Meta:
        db_table = 'awards'
        verbose_name = _("awards")
        verbose_name_plural = _("awards")
