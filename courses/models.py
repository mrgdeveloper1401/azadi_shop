from django.db import models
from django.utils import timezone
from shop.base import AUTH_USER_MODEL
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin


class CourseCategory(CreateMixin, UpdateMixin):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')
    icon = models.ImageField(upload_to='category_icon/%Y/%m/%d', blank=True, null=True)

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
    image = models.ImageField(upload_to='course_image/%Y/%m/%d', blank=True, null=True)
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
        # اگر قیمت دوره معین نشده باشد، یک استثناء در نظر میگیریم
        if self.price is None:
            raise ValueError("The course price cannot be None")

        # گرفتن تخفیف‌های فعال برای این دوره
        active_discounts = self.course_discount.filter(
            is_active=True,
            expired_date__gte=timezone.now()
        ).order_by('-created_at')

        # پیش‌فرض: قیمت نهایی برابر با قیمت اصلی دوره است
        total_price = self.price

        if active_discounts.exists():
            # استفاده از جدیدترین تخفیف فعال
            discount = active_discounts.first()

            if discount.type == 'درصدی':
                # اعمال تخفیف درصدی
                discount_value = min(max(discount.value, 0), 100)
                discount_amount = (self.price * discount_value) / 100
                total_price = self.price - discount_amount

            elif discount.type == 'مقدار':
                # اعمال تخفیف مقداری
                discount_amount = min(discount.value, self.price)
                total_price = self.price - discount_amount

        # قیمت نهایی نباید منفی باشد
        return max(total_price, 0)


class DiscountCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_discount')

    TYPE_CHOICES = (
        ('بدون تخفیف', 'بدون تخفیف'),
        ('درصدی', 'درصدی'),
        ('مقدار', 'مقدار'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='بدون تخفیف')
    value = models.PositiveIntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField()

    class Meta:
        ordering = ("-created_at",)

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
