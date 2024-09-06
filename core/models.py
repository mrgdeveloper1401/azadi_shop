from django.db import models
from django_jalali.db.models import jDateTimeField
from jdatetime import datetime


# Create your models here.
class CreateMixin(models.Model):
    created_at = jDateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = jDateTimeField(auto_now=True)

    class Meta:
        abstract = True