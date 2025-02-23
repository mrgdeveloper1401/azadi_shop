from django.db import models
from django.utils.text import slugify
from treebeard.mp_tree import MP_Node
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from core.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class CategoryNode(MP_Node, CreateMixin, UpdateMixin, SoftDeleteMixin):
    category_name = models.CharField(_('نام دسته بندی'), max_length=50)
    node_order_by = ['category_name']
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'blog_category'
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")


class Post(CreateMixin, UpdateMixin, SoftDeleteMixin):
    author = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='user_posts',
                               limit_choices_to={'is_active': True, "is_staff": True},
                               verbose_name=_("نویسنده"))
    category = models.ManyToManyField(CategoryNode, related_name='posts', verbose_name=_("دسته بندی"))
    post_title = models.CharField(_('عنوان پست'), max_length=255, unique=True)
    tiny_title = models.CharField(_("عنوان کوتاه پست"), max_length=50, blank=True, null=True,
                                  help_text=_("عنوان خلاصه شده پست هست و حداکثر 50 تا کاراتر میتوان نوشت"))
    introduction = models.CharField(_("مقدمه"), max_length=255, blank=True, null=True)
    slug = models.SlugField(_('اسلاگ'), max_length=255, allow_unicode=True, blank=True)
    post = CKEditor5Field(config_name="extends")
    is_publish = models.BooleanField(_("قابل انتشار"), default=False)
    view_number = models.PositiveIntegerField(_('تعداد بازدید'), default=0, editable=False)
    post_image = models.ImageField(_("عکس کاور پست"))

    def __str__(self):
        return self.post_title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.post_title, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'پست وبلاگ'
        verbose_name_plural = 'پست های وبلاگ'
        db_table = 'blog_post'
        ordering = ('-created_at',)
