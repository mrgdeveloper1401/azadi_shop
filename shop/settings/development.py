# from celery.schedules import crontab

from shop.base import *


DEBUG = True

ALLOWED_HOSTS = []

# CELERY_BROKER_URL = 'redis://0.0.0.0:6380/1'
# result_backend = 'redis://0.0.0.0:6380/1'
# broker_connection_retry_on_startup = True
# timezone = 'Asia/Tehran'
# enable_utc = True
# worker_prefetch_multiplier = 1
# result_expires = 120
# task_always_eager = False
#
# CELERY_BEAT_SCHEDULE = {
#     'delete_otp_code': {
#         'task': 'users.tasks.delete_otp_code',
#         'schedule': crontab(minute='*/2')
#     }
# }
