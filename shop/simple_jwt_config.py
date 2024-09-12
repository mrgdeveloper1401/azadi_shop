from jdatetime import timedelta
from os import environ

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    "AUTH_HEADER_TYPES": 'JWT',
    "SIGNING_KEY": environ.get("SECRET_KEY"),
}
