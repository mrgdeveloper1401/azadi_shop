"""
WSGI config for shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from decouple import config

debug_mode = config('DEBUG', default=True, cast=bool)
print(debug_mode)
if debug_mode:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.production')

application = get_wsgi_application()
