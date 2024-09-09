from django.db import models
from shop.base import AUTH_USER_MODEL
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from core.models import CreateMixin, UpdateMixin


class CourseCategory(MP_Node):
    name = models.CharField(max_length=200)
    icon = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='image_category',
                             blank=True, null=True)

    class Meta:
        db_table = "category"
        verbose_name = _('category')
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Course(CreateMixin, UpdateMixin):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name="user_course", on_delete=models.PROTECT,
                             limit_choices_to={"is_staff": True, "is_superuser": True})
    category = models.ForeignKey(CourseCategory, related_name="category_course", on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    video = models.FileField(upload_to='videos/%Y/%m/%d', blank=True, null=True)
    image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name="course_image",
                              blank=True, null=True)
    sales = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'course'
        verbose_name = _('course')
        verbose_name_plural = _("courses")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        discount = self.course_discount.all()
        f = self.price
        for d in discount:
            f = d.calc_price(f)
        return f


class DiscountCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_discount')

    TYPE_CHOICES = (
        ('بدون تخفیف', 'بدون تخفیف'),
        ('درصدی', 'درصدی'),
        ('مقدار', 'مقدار'),
    )

    discount_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='بدون تخفیف')
    value = models.PositiveIntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField()

    def calc_price(self, price):
        if self.discount_type == "درصدی":
            return (price * self.value) / 100
        if self.discount_type == "مقدار":
            return price - self.value
        else:
            res = price
        return max(res, 0)

    class Meta:
        db_table = "discount"
        verbose_name = _('discount')
        verbose_name_plural = _("discounts")

    def __str__(self):
        return self.course.name


class Comment(CreateMixin, UpdateMixin):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment',
                             limit_choices_to={"is_active": True, "is_verified": True})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_comment')
    body = models.TextField(max_length=2048)
    public = models.BooleanField(default=True)
    reply_to = models.ForeignKey('self', blank=True, null=True, related_name="reply_comment",
                                 on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.user} - {self.course.name} - {self.body[:20]}"

    class Meta:
        db_table = 'comment'
        verbose_name = _('comment')
        verbose_name_plural = _("comments")
