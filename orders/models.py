from django.db import models

from core.models import CreateMixin, UpdateMixin


class Order(CreateMixin, UpdateMixin):
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='orders',
                             limit_choices_to={'is_active': True, "is_verified": True, "is_deleted": False})
    course = models.ManyToManyField('courses.Course', related_name='course_items')
    payment_status = models.CharField(
        choices=[("complete", "complete"), ("pending", "pending"), ("failed", "failed")], max_length=8,
        default="pending",
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    def __str__(self):
        return f'{self.user.mobile_phone} {self.payment_status}'

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید'
        db_table = 'orders'
