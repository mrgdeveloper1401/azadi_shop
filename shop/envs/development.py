from shop.base import *

ALLOWED_HOSTS = []

SECRET_KEY = config('SECRET_KEY', cast=str)

# debug toolbar
INTERNAL_IPS = [
    # ...
    "127.0.0.1"
    # ...
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        "NAME": "azadidb",
        "PORT": "5432",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
    }
}

INSTALLED_APPS += [
    # "django_logging",
    'debug_toolbar',
]
MIDDLEWARE += [
    # debug toolbar
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# simple jwt config
SIMPLE_JWT['SIGNING_KEY'] = config("SECRET_KEY", cast=str)


# cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
    }
}
