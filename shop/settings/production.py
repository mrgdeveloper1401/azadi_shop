from shop.base import *
import dj_database_url


os.environ.setdefault('GDAL_LIBRARY_PATH', '/usr/lib/libgdal.so')

SECRET_KEY = config('DEBUG', default=True, cast=str)

ALLOWED_HOSTS = ["*"]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': os.environ.get('DATABASE_DB'),
#         'USER': os.environ.get('DATABASE_USER'),
#         'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
#         'HOST': os.environ.get('DATABASE_HOST'),
#         'PORT': os.environ.get('DATABASE_PORT'),
#     }
# }

DATABASES = {
    'default': dj_database_url.config(default=config('LIARA_DATABASE_URL', cast=str))
}


# cors allowed origin config
CORS_ALLOWED_ORIGINS = [
    '0.0.0.0:3000',
    "0.0.0.0:3001"
    "0.0.0.0:5000",
    "0.0.0.0:5001",
    "0.0.0.0:8000",
    "0.0.0.0:8001",
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
