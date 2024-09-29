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

# DATABASES = {
#     'default': {
#         'ENGINE': "django.db.backends.postgresql",
#         "NAME": "azadi",
#         "PORT": "5432",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": "localhost",
#     }
# }

INSTALLED_APPS += [
    "django_logging",
]
MIDDLEWARE += ['django_logging.middleware.RequestLogMiddleware']

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
}