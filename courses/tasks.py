from celery import shared_task

from .models import DiscountCourse
from core.datetime_config import now
from shop.celery_config import app


@app.task()
def remove_expired_discounts():
    DiscountCourse.objects.filter(expired_date__lt=now()).delete()
