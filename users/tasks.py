from __future__ import absolute_import, unicode_literals
from celery import shared_task

from users.models import Otp


@shared_task
def delete_otp_code():
    return Otp.objects.delete_otp()
