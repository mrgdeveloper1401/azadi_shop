from shop.base import *

DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = config('SECRET_KEY', default=True, cast=str)

# debug toolbar
INTERNAL_IPS = [
    # ...
    "127.0.0.1"
    # ...
]

DATABASES = {
    'default': {
        'ENGINE': "django.contrib.gis.db.backends.postgis",
        "NAME": "azadi",
        "PORT": "5432",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
    }
}