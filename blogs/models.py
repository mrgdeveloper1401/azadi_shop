from django.db import models
from django.utils.text import slugify
from treebeard.mp_tree import MP_Node
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin


class CategoryNode(MP_Node):
    category_name = models.CharField(_('نام دسته بندی'), max_length=50, unique=True)
    category_slug = models.SlugField(_('اسلاگ دسته بندی'), max_length=50, allow_unicode=True, unique=True)
    node_order_by = ['category_name']

    def __str__(self):
        return self.category_name

    @property
    def children(self):
        return self.get_children().values('category_name')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'blog_category'
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")


class Post(CreateMixin, UpdateMixin):
    author = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='user_posts',
                               limit_choices_to={'is_active': True, "is_staff": True, "is_verified": True},
                               verbose_name=_("نویسنده"))
    category = models.ManyToManyField(CategoryNode, related_name='posts', verbose_name=_("دسته بندی"))
    post_title = models.CharField(_('عنوان پست'), max_length=255, unique=True)
    slug = models.SlugField(_('اسلاگ'), max_length=255, unique=True, allow_unicode=True)
    post_body = models.TextField(_('متن پست'))
    is_publish = models.BooleanField(_("قابل انتشار"), default=False)
    view_number = models.PositiveIntegerField(_('تعداد بازدید'), default=0, editable=False)

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name = 'پست وبلاگ'
        verbose_name_plural = 'پست های وبلاگ'
        db_table = 'blog_post'
