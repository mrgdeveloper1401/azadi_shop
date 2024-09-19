from jdatetime import datetime, timedelta
from pytz import timezone


def now():
    return datetime.now(timezone('Asia/Tehran'))


def after_two_minute():
    return datetime.now() + timedelta(minutes=2)
