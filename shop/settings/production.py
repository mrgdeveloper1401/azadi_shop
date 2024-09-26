from shop.base import *
import os

os.environ.get('GDAL_LIBRARY_PATH', '/usr/lib/libgdal.so')


DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASE_DB'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8001',
    'http://localhost:8002',
    'http://localhost:8003',
    'http://localhost:8004',
    'http://localhost:8005',
    'http://127.0.0.1:8001',
    'http://127.0.0.1:8002',
    'http://127.0.0.1:8003',
    'http://127.0.0.1:8004',
    'http://127.0.0.1:8005',
]
