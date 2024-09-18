from django.core.management.base import BaseCommand

from users.models import Otp
from core.datetime_config import now


class Command(BaseCommand):
    help = 'Remove expired OTPs'

    def handle(self, *args, **options):
        expire_otp = Otp.objects.filter(expired_at__lt=now).delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully removed {expire_otp} expired OTPs'))
