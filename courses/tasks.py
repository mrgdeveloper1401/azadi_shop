from celery import shared_task

from .models import DiscountCourse
from django.utils.timezone import now


@shared_task
def remove_expired_discounts():
    return DiscountCourse.objects.filter(expired_date__lt=now()).delete()
