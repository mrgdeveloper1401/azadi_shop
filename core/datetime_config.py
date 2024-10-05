from django.utils import timezone as django_timezone
from pytz import timezone
from datetime import timedelta


def after_two_minute():
    return django_timezone.now() + timedelta(minutes=2)
