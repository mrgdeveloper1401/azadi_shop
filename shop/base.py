from pathlib import Path
from datetime import timedelta
from decouple import config
import os

from shop.ckeditor_config import CKEDITOR_5_CONFIGS, customColorPalette

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = config('DEBUG', default=True, cast=bool)

THIRD_PARTY_APPS = [
    'users.apps.UsersConfig',
    'courses.apps.CoursesConfig',
    "images.apps.ImagesConfig",
    'orders.apps.OrdersConfig',
    "professors.apps.ProfessorsConfig",
    'payments.apps.PaymentsConfig',
    "main_settings.apps.MainSettingsConfig",
    "core.apps.CoreConfig",
    "blogs.apps.BlogsConfig",
    # "coupons.apps.CouponsConfig",
]

THIRD_PARTY_PACKAGE = [
    "rest_framework",
    'rest_framework_simplejwt',
    'drf_spectacular',
    "treebeard",
    "django_filters",
    "storages",
    "corsheaders",
    "import_export",
    "django_ckeditor_5"
]

INSTALLED_APPS = [
    # "unfold",
    # "unfold.contrib.filters",
    # "unfold.contrib.inlines",
    # "unfold.contrib.forms",
    # "unfold.contrib.import_export",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.gis',
    *THIRD_PARTY_APPS,
    *THIRD_PARTY_PACKAGE,

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # {
    #     'NAME': 'shop.uppercase_password_validator.UppercasePasswordValidator',
    # }
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = config("STATIC_URL", cast=str)
STATIC_ROOT = os.path.join(BASE_DIR / 'staticfiles')

MEDIA_URL = config("MEDIA_URL", cast=str)
MEDIA_ROOT = os.path.join(config("MEDIA_ROOT", cast=str), 'media')

# user
AUTH_USER_MODEL = 'users.User'

# spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'گروه اموزش انرژی',
    'DESCRIPTION': 'Your  description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# CELERY BEAT SCHEDULER
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Django-storages configuration
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    }
}

# rest framework config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# simple jwt config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    "AUTH_HEADER_TYPES": ('Bearer',),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# S3 Settings Based on AWS (optional)
AWS_ACCESS_KEY_ID = config("ARVAN_ACCESS_KEY", cast=str)
AWS_SECRET_ACCESS_KEY = config("ARVAN_SECRET_KEY", cast=str)
AWS_STORAGE_BUCKET_NAME = config('ARVAN_BUCKET_NAME', cast=str)
AWS_S3_ENDPOINT_URL = config("ARVAN_ENDPOINT", cast=str)
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_SERVICE_NAME = 's3'
AWS_S3_USE_SSL = True
AWS_S3_SECURE_URLS = True
AWS_DEFAULT_ACL = "public-read"

# django admin chart config
# ADMIN_CHARTS_NVD3_JS_PATH = 'bow/nvd3/build/nv.d3.js'
# ADMIN_CHARTS_NVD3_CSS_PATH = 'bow/nvd3/build/nv.d3.css'
# ADMIN_CHARTS_D3_JS_PATH = 'bow/d3/d3.js'
# BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')
# BOWER_INSTALLED_APPS = [
#     'd3#3.3.13',
#     'nvd3#1.7.1',
# ]
#
# STATICFILES_FINDERS = [
#     'djangobower.finders.BowerFinder',
# ]


# jet admin token
# JET_PROJECT = 'raminazadi_shop'
# JET_TOKEN = config("JET_TOKEN", cast=str)


# logging
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

# ckeditor 5
CKEDITOR_5_FILE_STORAGE = "storages.backends.s3.S3Storage"
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
