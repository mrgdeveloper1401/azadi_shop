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
SIMPLE_JWT['AUTH_COOKIE_SECURE'] = False,  # Whether the auth cookies should be secure (https:// only).
SIMPLE_JWT['AUTH_COOKIE_DOMAIN'] = None,     # A string like "example.com", or None for standard domain cookie.]

# cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
    }
}
