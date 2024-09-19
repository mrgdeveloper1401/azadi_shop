from django.db import models
from django_jalali.db.models import jDateTimeField
from jdatetime import datetime

from core.datetime_config import now


# Create your models here.
class CreateMixin(models.Model):
    created_at = jDateTimeField(default=now())

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = jDateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    deleted_at = jDateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    class Meta:
        abstract = True
