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
        "TIMEOUT": 750,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            "PICKLE_VERSION": -1,
            "SOCKET_CONNECT_TIMEOUT": 10,
            "SOCKET_TIMEOUT": 10,
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": True,
            "CONNECTION_POOL_KWARGS": {'max_connections': 100, "retry_on_timeout": True},
            "PARSER_CLASS": "redis.connection.HiredisParser",

        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
SESSION_REDIS_TTL = 60 * 15

STORAGES['staticfiles'] = {
    'BACKEND': "whitenoise.storage.CompressedManifestStaticFilesStorage"
}

# MIDDLEWARE += [
#     "django.middleware.cache.UpdateCacheMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.cache.FetchFromCacheMiddleware",
# ]

