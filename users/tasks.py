from celery import shared_task
# from django.utils.timezone import now
# from rest_framework.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

from shop.utils import send_sms
# from core.datetime_config import after_two_minute


# @shared_task
# def delete_otp_code():
#     Otp.objects.filter(expired_at__lt=now()).delete()


# def schedule_otp(request):
#     interval, _ = IntervalSchedule.objects.get_or_create(
#         every=2,
#         period=IntervalSchedule.MINUTES,
#     )
#     PeriodicTask.objects.create(
#         interval=interval,
#         name="schedule otp code",
#         task="users.tasks.delete_otp_code",
#     )

@shared_task
def send_otp_code(mobile_phone, code):
    send_sms(mobile_phone, code)
