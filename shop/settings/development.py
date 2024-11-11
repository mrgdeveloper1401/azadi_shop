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
    # "django_ckeditor_5",
]
MIDDLEWARE += [
    # debug toolbar
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    # package dj-logging
    # 'django_logging.middleware.RequestLogMiddleware',

    # chash with django redis
    # "django.middleware.cache.UpdateCacheMiddleware",
    # "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",

    # whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# simple jwt config
SIMPLE_JWT['SIGNING_KEY'] = config("SECRET_KEY", cast=str)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "TIMEOUT": 900,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "IGNORE_EXCEPTIONS": False,
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
DJANGO_REDIS_LOGGER = 'azadi_redis_logger'

# logging in django, whit third party package
# log_file = BASE_DIR / "logs"
# DJANGO_LOGGING = {
#     "AUTO_INITIALIZATION_ENABLE": True,
#     "INITIALIZATION_MESSAGE_ENABLE": True,
#     "LOG_FILE_LEVELS": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
#     "LOG_DIR": f"{log_file}",
#     "LOG_FILE_FORMATS": {
#         "DEBUG": 1,
#         "INFO": 1,
#         "WARNING": 1,
#         "ERROR": 1,
#         "CRITICAL": 1,
#     },
#     "LOG_CONSOLE_LEVEL": "DEBUG",
#     "LOG_CONSOLE_FORMAT": 1,
#     "LOG_CONSOLE_COLORIZE": True,
#     "LOG_DATE_FORMAT": "%Y-%m-%d %H:%M:%S",
#     "LOG_EMAIL_NOTIFIER": {
#         "ENABLE": False,
#         "NOTIFY_ERROR": False,
#         "NOTIFY_CRITICAL": False,
#         "LOG_FORMAT": 1,
#         "USE_TEMPLATE": True,
#     },
#     "LOGGERS": {
#         "azadi_redis_logger": {
#             "level": "ERROR",
#             "handlers": ["console", "file"],
#             "propagate": True,
#         }
#     }
# }

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
