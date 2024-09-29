"""
ASGI config for shop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from decouple import config
from django.core.asgi import get_asgi_application

debug_mode = config('DEBUG', default=True, cast=bool)

if debug_mode:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.development')
if not debug_mode:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.production')

application = get_asgi_application()
