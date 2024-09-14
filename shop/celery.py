from __future__ import absolute_import, unicode_literals
from celery import Celery

from os import environ
from shop.base import DEBUG

if DEBUG:
    environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings.development'
if not DEBUG:
    environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings.production'

app = Celery('shop')
app.conf.enable_utc = False
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    with open('celery_log.log', 'a') as f:
        print('Request: {0!r}'.format(self.request), file=f)