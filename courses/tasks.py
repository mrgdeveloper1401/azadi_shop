from celery import shared_task

from .models import DiscountCourse
from core.datetime_config import now


@shared_task
def remove_expired_discounts():
    DiscountCourse.objects.filter(expired_date__lt=now).delete()
