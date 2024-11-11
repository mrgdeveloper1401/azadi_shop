from shop.base import *
import dj_database_url

SECRET_KEY = config('DEPLOY_SECRET_KEY', cast=str)

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL', cast=str))
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
        "LOCATION": config('REDIS_URL', cast=str),
        'TIMEOUT': 750,
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
SESSION_REDIS_TTL = 750

MIDDLEWARE += [
    # "django.middleware.cache.UpdateCacheMiddleware",
    # "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    # cors-header
    "corsheaders.middleware.CorsMiddleware",
]

# with logging django
log_dir = os.path.join(BASE_DIR / 'general_log_django')
os.makedirs(log_dir, exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(levelname)s %(reset)s%(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    'filters': {
        'require_debug_true': {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "color",
            "filters": ["require_debug_true"],
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "color",
            "filename": os.path.join(BASE_DIR / log_dir / 'info_file.log')
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "color",
            "filename": os.path.join(BASE_DIR / log_dir / 'error_file.log')
        },
        "warning_file": {
            "level": "WARN",
            "class": "logging.FileHandler",
            "formatter": "color",
            "filename": os.path.join(BASE_DIR / log_dir / 'warning_file.log')
        },
        "critical_file": {
            "level": "CRITICAL",
            "class": "logging.FileHandler",
            "formatter": "color",
            "filename": os.path.join(BASE_DIR / log_dir / 'critical_file.log')
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "info_file", "warning_file", "critical_file", "error_file"],
            'propagate': True,
        }
    }
}
