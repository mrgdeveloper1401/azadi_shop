from shop.base import *
import os

os.environ.get('GDAL_LIBRARY_PATH', '/usr/lib/libgdal.so')


DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_DB'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}

CORS_ALLOWED_ORIGINS = [
    'https://localhost:8000',
    "https://127.0.0.1:8000",
]

