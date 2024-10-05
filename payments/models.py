from django.db import models
# from orders.models import Order
from django.utils.translation import gettext_lazy as _

from core.models import CreateMixin, UpdateMixin
from shop.base import AUTH_USER_MODEL
from django.utils.timezone import now


# Create your models here.
class Payment(CreateMixin, UpdateMixin):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    order_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='course_payment')
    final_price = models.DecimalField(max_digits=12, decimal_places=3)
    discount_value = models.DecimalField(max_digits=12, decimal_places=3)
    license_key = models.TextField(blank=True, null=True)

    def generate_order_number(self):
        text = 'shop'
        d = now().date()
        res = text + '-' + d + self.id
        return res

    def save(self, *args, **kwargs):
        self.order_number = self.generate_order_number()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'payments'
        verbose_name = _("payments")
        verbose_name_plural = _("payments")
