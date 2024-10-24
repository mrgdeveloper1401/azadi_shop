from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from core.models import CreateMixin, UpdateMixin
from courses.managers import CourseManager
from courses.managers import DiscountManager


class CourseCategory(MP_Node):
    name = models.CharField(_('نام دسته بندی'), max_length=200, unique=True)
    icon = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name='image_category',
                             blank=True, null=True, verbose_name=_("عکس دسته بندی"))
    # is_public = models.BooleanField(default=True)
    slug = models.SlugField(_('اسلاگ'), max_length=200, allow_unicode=True, unique=True)
    # objects = CategoryManager()

    @property
    def children(self):
        return self.get_children().values('name')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "category"
        verbose_name = _('دسته بندی دوره')
        verbose_name_plural = _("دسته بندی دوره ها")

    def __str__(self):
        return self.name


class Course(CreateMixin, UpdateMixin):
    professor = models.ForeignKey('professors.Professor', related_name="professor_course", on_delete=models.PROTECT,
                                  limit_choices_to={"is_active": True}, verbose_name=_("استاد"))
    category = models.ManyToManyField(CourseCategory, related_name="category_course", verbose_name=_("دسته بندی"))
    name = models.CharField(_('نام محصول'), max_length=255)
    slug = models.SlugField(_('اسلاگ'), unique=True, max_length=255, allow_unicode=True)
    # description = CKEditor5Field('Text', blank=True, null=True, config_name='extends')
    description = models.TextField(_('درباره دوره'), blank=True, null=True)
    price = models.DecimalField(_('قیمت دوره'), decimal_places=2, max_digits=12,
                                validators=[MinValueValidator(Decimal(0))])
    video = models.FileField(_('فیلم معرفی دوره'), upload_to='videos/%Y/%m/%d', blank=True, null=True)
    image = models.ForeignKey('images.Image', on_delete=models.PROTECT, related_name="course_image",
                              verbose_name=_("عکس دوره"))
    sale_number = models.PositiveSmallIntegerField(_('تعداد فروش دوره'), default=0, editable=False)
    is_sale = models.BooleanField(_('قابل فروش'), default=True,
                                  help_text=_("if is sale is true, this course can be sale ,otherwise this course "
                                              "can't"))
    is_free = models.BooleanField(_('رایگان'), default=False)
    is_active = models.BooleanField(_('فعال'), default=True)
    total_like = models.PositiveIntegerField(_("تعداد کاربران پسندیده شده"), default=0, editable=False)

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
        elif self.is_free:
            self.price = 0
        super().save(*args, **kwargs)

    @property
    def show_image_url(self):
        return self.image.image.url

    @property
    def calc_final_price(self):
        discounts = self.course_discount.all()
        final_price = self.price
        if discounts.exists():
            for d in discounts:
                if d.discount_type == 'درصدی':
                    f = (d.value * self.price) / 100
                else:
                    f = self.price - d.value
                return max(f, 0)
        else:
            return final_price

    @property
    def comment_number(self):
        return self.course_comment.count()

    def __str__(self):
        return self.name


class DiscountCourse(CreateMixin, UpdateMixin):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_discount',
                               limit_choices_to={"is_active": True, "is_sale": True, 'is_free': False},
                               verbose_name=_("دوره"))

    TYPE_CHOICES = (
        ('درصدی', 'درصدی'),
        ('مقدار', 'مقدار'),
    )

    discount_type = models.CharField(_('نوع تخفیف'), max_length=10, choices=TYPE_CHOICES, default='بدون تخفیف')
    value = models.PositiveIntegerField(_('مقدار تخفیف'))
    is_active = models.BooleanField(_('فعال'), default=True)
    expired_date = models.DateTimeField(_("زمان انتقضا"))

    objects = DiscountManager()

    def __str__(self):
        return self.course.name

    class Meta:
        db_table = "discount"
        verbose_name = _('تخفیف')
        verbose_name_plural = _("تخفیف ها")


class Comment(CreateMixin, UpdateMixin):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_comment',
                             limit_choices_to={"is_active": True, "is_verified": True}, verbose_name=_("کاربر"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_comment',
                               limit_choices_to={"is_active": True, "is_sale": True}, verbose_name=_("دوره"))
    body = models.TextField(_("متن کامنت"), max_length=2048)
    public = models.BooleanField(_('انتشار'), default=True)
    # reply_to = models.ForeignKey('self', blank=True, null=True, related_name="reply_comment",
    #                              on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True,
                                              null=True,
                                              help_text=_("Enter a score of 1 to 5"),
                                              verbose_name=_("امتیاز"))
    # admin_response = CKEditor5Field(blank=True, null=True, config_name='extends')
    admin_response = models.TextField(_('پاسخ ادمین'), blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.course.name} - {self.body[:20]}"

    class Meta:
        db_table = 'comment'
        verbose_name = _('نظر')
        verbose_name_plural = _("نظرات")


class Like(CreateMixin, UpdateMixin):
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='user_like',
                             limit_choices_to={'is_active': True, "is_verified": True}, verbose_name=_("کاربر"))
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='course_like',
                               limit_choices_to={'is_active': True}, verbose_name=_("دوره"))
    dislike = models.BooleanField(_('عدم پسندیدن'), default=False)

    def __str__(self):
        return f"{self.user.mobile_phone} {self.course.name}"

    class Meta:
        db_table = 'like'
        verbose_name = _('لایک دوره')
        verbose_name_plural = _("لایک های دوره")
        unique_together = (("user", "course"),)
