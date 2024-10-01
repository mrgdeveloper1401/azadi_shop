from shop.base import *

# from shop.ckeditor_config import CKEDITOR_5_CONFIGS, customColorPalette


ALLOWED_HOSTS = ['*']

SECRET_KEY = config('SECRET_KEY', cast=str)

# debug toolbar
INTERNAL_IPS = [
    # ...
    "127.0.0.1"
    # ...
]

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        "NAME": "azadi",
        "PORT": "5432",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
    }
}

INSTALLED_APPS += [
    "django_logging",
    # "django_ckeditor_5",
]
MIDDLEWARE += ['django_logging.middleware.RequestLogMiddleware']


# simple jwt config
SIMPLE_JWT['SIGNING_KEY'] = config("SECRET_KEY", cast=str)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
            "SOCKET_CONNECT_TIMEOUT": 10,
            "SOCKET_TIMEOUT": 5,
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": True,
            "CONNECTION_POOL_KWARGS": {'max_connections': 100, "retry_on_timeout": True},
            "PARSER_CLASS": "redis.connection.HiredisParser",
            # "SERIALIZER": "django_redis.serializers.msgpack.MSGPackSerializer",
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
DJANGO_REDIS_LOGGER = 'azadi_redis_logger'

STORAGES['staticfiles'] = {
    # "BACKEND": "django.core.files.storage.FileSystemStorage",
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
}

# logging in django
log_file = BASE_DIR / "logs"
res = log_file / f"logs_{now().strftime('%Y-%m-%d')}"
DJANGO_LOGGING = {
    "AUTO_INITIALIZATION_ENABLE": True,
    "INITIALIZATION_MESSAGE_ENABLE": True,
    "LOG_FILE_LEVELS": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    "LOG_DIR": f"{res}",
    "LOG_FILE_FORMATS": {
        "DEBUG": 1,
        "INFO": 1,
        "WARNING": 1,
        "ERROR": 1,
        "CRITICAL": 1,
    },
    "LOG_CONSOLE_LEVEL": "DEBUG",
    "LOG_CONSOLE_FORMAT": 1,
    "LOG_CONSOLE_COLORIZE": True,
    "LOG_DATE_FORMAT": "%Y-%m-%d %H:%M:%S",
    "LOG_EMAIL_NOTIFIER": {
        "ENABLE": False,
        "NOTIFY_ERROR": False,
        "NOTIFY_CRITICAL": False,
        "LOG_FORMAT": 1,
        "USE_TEMPLATE": True,
    },
    "LOGGERS": {
        "azadi_redis_logger": {
            "level": "ERROR",
            "handlers": ["console", "file"],
            "propagate": True,
        }
    }
}