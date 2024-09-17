from django.db import models
from django.utils import timezone
from ulid import ULID
from django.utils.translation import gettext_lazy as _

from shop.base import AUTH_USER_MODEL
from courses.models import Course
from core.models import CreateMixin, UpdateMixin


class Cart(CreateMixin, UpdateMixin):
    id = models.CharField(primary_key=True, editable=False, auto_created=True, verbose_name="ID", max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="cart user",
                             blank=True, null=True, related_name="user_cart")
    # cart_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'

    @property
    def generate_ulid(self):
        return str(ULID.from_datetime(timezone.now()))

    @property
    def total_price(self):
        price = [i.quantity * i.course.final_price for i in self.cart_item.all()]
        return sum(price)

    def save(self, *args, **kwargs):
        self.id = self.generate_ulid
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        db_table = 'cart'
        verbose_name = _('cart')
        verbose_name_plural = _('carts')


class CartItem(CreateMixin):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_cart_item')
    quantity = models.PositiveSmallIntegerField(default=1)

    @property
    def get_course_name(self):
        return self.course.name

    @property
    def item_price(self):
        price = self.course.price * self.quantity
        return price

    class Meta:
        db_table = 'cart_item'
        verbose_name = _('cart_item')
        verbose_name_plural = _('cart_items')
        unique_together = (('cart', 'course'),)
        ordering = ('-created_at',)


class Order(CreateMixin):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_order')

    class PaymentStatus(models.TextChoices):
        pending = 'pending', _('Pending')
        complete = 'complete', _('Complete')
        failed = 'failed', _('Failed')

    payment_status = models.CharField(_("payment status"), max_length=8, choices=PaymentStatus.choices,
                                      default=PaymentStatus.pending)

    def __str__(self):
        return f'{self.user} {self.payment_status} {self.created_at}'

    @property
    def order_total_price(self):
        price = [i.quantity * i.price for i in self.order_item.all()]
        return sum(price)

    class Meta:
        db_table = 'order'
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderItem(CreateMixin):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_item')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='course_order_item', blank=True,
                               null=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return f'{self.order} {self.course} {self.quantity}'

    class Meta:
        db_table = 'order_item'
        verbose_name = _('order_item')
        verbose_name_plural = _('order_items')
        unique_together = (('order', 'course'),)