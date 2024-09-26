from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import shared_task

from users.models import Otp
from core.datetime_config import now, after_two_minute


@shared_task()
def delete_otp_code():
    Otp.objects.filter(expired_at__lt=now()).delete()


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
