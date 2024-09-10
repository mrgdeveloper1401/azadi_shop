from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Cart
from users.models import UserAccount


@receiver(post_save, sender=UserAccount)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)