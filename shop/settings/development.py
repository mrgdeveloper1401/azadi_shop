# # from shop.base import *
# #
# # ALLOWED_HOSTS = []
# #
# # SECRET_KEY = config('SECRET_KEY', cast=str)
#
#
# # debug toolbar
# # INTERNAL_IPS = [
#     # ...
#     # "127.0.0.1"
#     # ...
# # ]
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         "NAME": "azadidb",
#         "PORT": "5432",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": "localhost",
#     }
# }
#
# INSTALLED_APPS += [
#     "django_logging",
#     'debug_toolbar',
#     # "django_ckeditor_5",
# ]
# MIDDLEWARE += [
#     # debug toolbar
#     "debug_toolbar.middleware.DebugToolbarMiddleware",
#     'django_logging.middleware.RequestLogMiddleware',
#     # chash with django redis
#     # "django.middleware.cache.UpdateCacheMiddleware",
#     # "django.middleware.common.CommonMiddleware",
#     # "django.middleware.cache.FetchFromCacheMiddleware",
#     # whitenoise
#     "whitenoise.middleware.WhiteNoiseMiddleware",
# ]
#
# # simple jwt config
# SIMPLE_JWT['SIGNING_KEY'] = config("SECRET_KEY", cast=str)
#
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/2",
#         "TIMEOUT": 300,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "SOCKET_CONNECT_TIMEOUT": 5,
#             "SOCKET_TIMEOUT": 5,
#             "IGNORE_EXCEPTIONS": False,
#         }
#     }
# }
#
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
# DJANGO_REDIS_LOGGER = 'azadi_redis_logger'
#
# # logging in django, whit third party package
# # log_file = BASE_DIR / "logs"
# # DJANGO_LOGGING = {
# #     "AUTO_INITIALIZATION_ENABLE": True,
# #     "INITIALIZATION_MESSAGE_ENABLE": True,
# #     "LOG_FILE_LEVELS": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
# #     "LOG_DIR": f"{log_file}",
# #     "LOG_FILE_FORMATS": {
# #         "DEBUG": 1,
# #         "INFO": 1,
# #         "WARNING": 1,
# #         "ERROR": 1,
# #         "CRITICAL": 1,
# #     },
# #     "LOG_CONSOLE_LEVEL": "DEBUG",
# #     "LOG_CONSOLE_FORMAT": 1,
# #     "LOG_CONSOLE_COLORIZE": True,
# #     "LOG_DATE_FORMAT": "%Y-%m-%d %H:%M:%S",
# #     "LOG_EMAIL_NOTIFIER": {
# #         "ENABLE": False,
# #         "NOTIFY_ERROR": False,
# #         "NOTIFY_CRITICAL": False,
# #         "LOG_FORMAT": 1,
# #         "USE_TEMPLATE": True,
# #     },
# #     "LOGGERS": {
# #         "azadi_redis_logger": {
# #             "level": "ERROR",
# #             "handlers": ["console", "file"],
# #             "propagate": True,
# #         }
# #     }
# # }
#
# # for upload with object storage
# AWS_S3_SECURE_URLS = False
