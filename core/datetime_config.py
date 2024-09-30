from django.utils import timezone as django_timezone
from pytz import timezone


def now():
    return django_timezone.now()


def after_two_minute():
    return now() + django_timezone.timedelta(minutes=2)
