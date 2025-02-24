from django.db import models
from hashlib import sha1
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin
from images.validators import validate_image_size


class Image(CreateMixin, UpdateMixin):
    title = models.CharField(_('عنوان عکس'), max_length=128, help_text=_("عنوانی برای عکس خود انتخاب کنید"))
    image = models.ImageField(_('عکس'), width_field="width", height_field="height", upload_to="images/%Y/%m/%d",
                              validators=[validate_image_size],
                              help_text=_("max size is 5 MG"))
    width = models.IntegerField(_('عرض اندازه عکس'), null=True, blank=True)
    height = models.IntegerField(_('طول اندازه عکس'), null=True, blank=True)
    file_hash = models.CharField(_('هش فایل عکس'), max_length=40, null=True, blank=True)
    file_size = models.PositiveIntegerField(_('حجم عکس'), null=True, blank=True, help_text=_("file size as xx.b"))

    @property
    def generate_hash(self):
        hasher = sha1()
        for c in self.image.chunks():
            hasher.update(c)
        return hasher.hexdigest()

    @property
    def image_url(self):
        return self.image.url

    def save(self, *args, **kwargs):
        self.file_hash = self.generate_hash
        self.file_size = self.image.size
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "image"
        verbose_name = _("عکس")
        verbose_name_plural = _("عکس ها")
