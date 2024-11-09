from shop.base import *
import dj_database_url

SECRET_KEY = config('DEPLOY_SECRET_KEY', cast=str)

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL', cast=str))
    #     'default': {
    #         'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #         'PORT': config("POSTDB_PORT", cast=int),
    #         "HOST": config('POSTDB_HOST', cast=str),
    #         "USER": config("POSTDB_USER", cast=str),
    #         "PASSWORD": config("POSTDB_PASSWORD", cast=str),
    #         'NAME': config("POSTDB_NAME", cast=str),
    #     }
}

# cors allowed origin config
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = '*'
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     "https://test-azadi.liara.run"
# ]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
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
SIMPLE_JWT['SIGNING_KEY'] = config('DEPLOY_SECRET_KEY', cast=str)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('LIARA_REDIS_URL', cast=str),
        'TIMEOUT': 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 10,
            "SOCKET_TIMEOUT": 5,
            "COMPRESSOR": "django_redis.compressors.zstd.ZStdCompressor",
            "IGNORE_EXCEPTIONS": False,
            "CONNECTION_POOL_KWARGS": {
                'max_connections': 100,
                "retry_on_timeout": True,
            },
            "SERIALIZER": "django_redis.serializers.msgpack.MSGPackSerializer",
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
SESSION_REDIS_TTL = 300

MIDDLEWARE += [
    # "django.middleware.cache.UpdateCacheMiddleware",
    # "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    # cors-header
    "corsheaders.middleware.CorsMiddleware",
]
