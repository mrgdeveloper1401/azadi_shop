from celery import shared_task

from courses.models import DiscountCourse
from django.utils.timezone import now


@shared_task
def remove_expired_discounts():
    DiscountCourse.objects.filter(expired_date__lt=now()).delete()
