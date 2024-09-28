from celery import Celery
from decouple import config
from os import environ


DEBUG = config('DEBUG', default=True, cast=str)

if DEBUG:
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.development')
if not DEBUG:
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.production')

app = Celery('shop')
app.config_from_object('shop.celery_config_redis')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    with open('celery_log.log', 'a') as f:
        print('Request: {0!r}'.format(self.request), file=f)
