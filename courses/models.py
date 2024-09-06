from django.db import models
from django.utils import timezone
from slugify import slugify
from shop.base import AUTH_USER_MODEL


class CourseCategory(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False)
    icon = models.ImageField(upload_to='icons/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class Course(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name="courses", on_delete=models.CASCADE)
    category = models.ForeignKey(CourseCategory, related_name="courses", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    desc = models.TextField(blank=False, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    sales = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Course.objects.get(pk=self.pk).name != self.name):
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def get_total_price(self):
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


class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ucomment')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ccomment')
    body = models.TextField(max_length=2048)
    admin_response = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user} - {self.course.name} - {self.body[:20]}"

    class Meta:
        ordering = ['-created']
