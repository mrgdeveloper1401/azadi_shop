from django.db import models
from orders.models import Order
import random


# Create your models here.

# Order id
# Amount
# Status
# Tracking code


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('completed', 'completed')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    tracking_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def generate_tracking_code(self):
        tracking_code = random.randint(100000, 999999)
        return tracking_code
