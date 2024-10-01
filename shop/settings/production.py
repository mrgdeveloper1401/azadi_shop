from shop.base import *
import dj_database_url

# os.environ.setdefault('GDAL_LIBRARY_PATH', '/usr/lib/libgdal.so')

SECRET_KEY = config('LIARA_PRO_SECRET_KEY', cast=str)

ALLOWED_HOSTS = ["*"]


DATABASES = {
    # private url
    'default': dj_database_url.config(default=config('DATABASE_URL', cast=str))
    # public url
    # 'default': dj_database_url.config(default=config('PUBLIC_DATABASE_URL', cast=str))
}

# cors allowed origin config
CORS_ALLOWED_ORIGINS = [
    "https://azadi-shop.liara.run",
]


# ssl config
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_REFERRER_POLICY = "strict-origin"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# # simple jwt config
SIMPLE_JWT['SIGNING_KEY'] = config('LIARA_PRO_SECRET_KEY', cast=str)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config("LIARA_REDIS_URL"),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

SESSION_REDIS_TTL = 60 * 15

STORAGES['staticfiles'] = {
    'BACKEND': "whitenoise.storage.CompressedManifestStaticFilesStorage"
}
