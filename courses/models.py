from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.timezone import now

from shop.base import AUTH_USER_MODEL
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from core.models import CreateMixin, UpdateMixin
from courses.managers import CategoryManager, CourseManager
from courses.managers import DiscountManager


class CourseCategory(MP_Node):
    name = models.CharField(max_length=200, unique=True)
    icon = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='image_category',
                             blank=True, null=True)
    is_public = models.BooleanField(default=True)

    objects = CategoryManager()

    class Meta:
        db_table = "category"
        verbose_name = _('category')
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Course(CreateMixin, UpdateMixin):
    professor = models.ForeignKey('professors.Professor', related_name="professor_course", on_delete=models.PROTECT,
                                  limit_choices_to={"is_active": True, })
    category = models.ForeignKey(CourseCategory, related_name="category_course", on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal(0))],)
    video = models.FileField(upload_to='videos/%Y/%m/%d', blank=True, null=True)
    image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name="course_image",
                              blank=True, null=True)
    sale_number = models.PositiveSmallIntegerField(default=0)
    is_sale = models.BooleanField(default=True,
                                  help_text=_("if is sale is true, this course can be sale ,otherwise this course "
                                              "can't"))
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CourseManager()

    class Meta:
        db_table = 'course'
        verbose_name = _('course')
        verbose_name_plural = _("courses")
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        if self.price == 0:
            self.is_free = True
        super().save(*args, **kwargs)

    @property
    def show_image_url(self):
        return self.image.image.url

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        # discount = self.course_discount.filter(is_active=True, expired_date__gt=now())
        discount = self.course_discount.all()
        f = self.price
        for d in discount:
            f = d.calc_price(f)
        return f


class DiscountCourse(CreateMixin, UpdateMixin):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_discount',
                               limit_choices_to={"is_active": True})

    TYPE_CHOICES = (
        ('درصدی', 'درصدی'),
        ('مقدار', 'مقدار'),
    )

    discount_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='بدون تخفیف')
    value = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField()

    objects = DiscountManager()

    def __str__(self):
        return self.course.name

    def calc_price(self, price):
        if self.discount_type == "درصدی":
            calc_price = (price * self.value) / 100
            return price - calc_price
        if self.discount_type == "مقدار":
            return price - self.value
        else:
            res = price
        return max(res, 0)

    def clean(self):
        if DiscountCourse.objects.filter(course=self.course).exists():
            raise ValidationError({"course": _("course already exists")})

    class Meta:
        db_table = "discount"
        verbose_name = _('discount')
        verbose_name_plural = _("discounts")


class Comment(CreateMixin, UpdateMixin):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment',
                             limit_choices_to={"is_active": True, "is_verified": True})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_comment')
    body = models.TextField(max_length=2048)
    public = models.BooleanField(default=True)
    # reply_to = models.ForeignKey('self', blank=True, null=True, related_name="reply_comment",
    #                              on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True,
                                              null=True,
                                              help_text=_("Enter a score of 1 to 5"))

    def __str__(self) -> str:
        return f"{self.user} - {self.course.name} - {self.body[:20]}"

    class Meta:
        db_table = 'comment'
        verbose_name = _('comment')
        verbose_name_plural = _("comments")
