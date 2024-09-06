from celery import Celery

from os import environ

environ['DJANGO_SETTINGS_MODULE'] = 'shop.settings.development'

app = Celery('shop')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
