from django.db import models
from django.utils.translation import gettext_lazy as _
# from django_jalali.db.models import jDateTimeField

from core.models import CreateMixin, UpdateMixin
# Create your models here.


class Coupon(CreateMixin, UpdateMixin):
    code = models.CharField(_("coupon code"), max_length=30, unique=True)
    use_number = models.PositiveSmallIntegerField(default=0)
    max_used = models.PositiveSmallIntegerField(default=0)
    used_user = models.ManyToManyField('users.UserAccount', related_name='coupons', blank=True)
    is_active = models.BooleanField(default=False)

    class CouponChoices(models.TextChoices):
        amount = 'amount', _("مقدار")
        percent = 'percent', _("درصدی")
    coupon_type = models.CharField(_("coupon type"), max_length=8, choices=CouponChoices.choices)
    coupon_amount = models.PositiveIntegerField(_("coupon amount"))
