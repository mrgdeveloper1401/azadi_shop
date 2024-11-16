from django.db import models
# from orders.models import Order
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin
from shop.base import AUTH_USER_MODEL
from datetime import datetime


# Create your models here.
class Payment(CreateMixin, UpdateMixin):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='course_payment')
    final_price = models.DecimalField(max_digits=12, decimal_places=3)
    # discount_value = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    license_key = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'payments'
        verbose_name = _("پرداخت")
        verbose_name_plural = _("پرداخت ها")
