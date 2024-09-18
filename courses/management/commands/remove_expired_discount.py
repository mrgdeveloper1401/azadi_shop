from django.core.management.base import BaseCommand

from courses.models import DiscountCourse
from core.datetime_config import now


class Command(BaseCommand):
    help = 'Remove expired discounts'

    def handle(self, *args, **options):
        expire_discount = DiscountCourse.objects.filter(expired_date__lt=now).delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully removed {expire_discount} expired discounts'))

