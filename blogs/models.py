from django.db import models
from django.utils.text import slugify
from treebeard.mp_tree import MP_Node
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin, SoftDeleteMixin


class CategoryNode(CreateMixin, UpdateMixin):
    category_name = models.CharField(max_length=50, unique=True)
    category_slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children',
                               blank=True, null=True, verbose_name=_("دسته بندی والد"))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'blog_category'
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Post(CreateMixin, UpdateMixin, SoftDeleteMixin):
    author = models.ForeignKey('users.UserAccount', on_delete=models.PROTECT, related_name='user_posts',
                               limit_choices_to={'is_active': True, "is_staff": True, "is_superuser": True},
                               verbose_name=_("نویسنده"))
    category = models.ManyToManyField(CategoryNode, related_name='posts', verbose_name=_("دسته بندی"))
    post_title = models.CharField(_('عنوان پست'), max_length=255, unique=True)
    slug = models.SlugField(_('اسلاگ'), max_length=255, unique=True, allow_unicode=True)
    post_body = models.TextField(_('متن پست'))
    # post_image = models.ManyToManyField('BlogPostImage', related_name='m2m_post_images',
    #                                     verbose_name=_("عکس های پست"))
    is_publish = models.BooleanField(_("قابل انتشار"), default=False)
    view_number = models.PositiveIntegerField(_('تعداد بازدید'), default=0)

    def __str__(self):
        return f'{self.author.get_full_name} {self.post_title}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        db_table = 'posts'


class BlogPostImage(CreateMixin, UpdateMixin):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='fk_blog_post', verbose_name=_("پست"))
    image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='fk_blog_post_image',
                              verbose_name=_("عکس"))
    is_active = models.BooleanField(_('فعال بودن'), default=True)

    def __str__(self):
        return self.post.post_title

    class Meta:
        db_table = 'blog_post_images'
        verbose_name = _("'Blog Post Image'")
        verbose_name_plural = _("Blog Post Images")
