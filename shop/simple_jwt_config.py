from jdatetime import timedelta
from shop.base import SECRET_KEY

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    "SIGNING_KEY": SECRET_KEY,
}
