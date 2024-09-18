from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .models import DiscountCourse


@shared_task
def remove_expired_discounts():
    now = timezone.now()
    DiscountCourse.objects.filter(expired_date__lt=now).delete()
