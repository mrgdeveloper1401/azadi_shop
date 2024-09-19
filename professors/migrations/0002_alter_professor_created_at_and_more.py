# Generated by Django 5.0.8 on 2024-09-19 10:47

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("professors", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="professor",
            name="created_at",
            field=django_jalali.db.models.jDateTimeField(
                default=datetime.datetime(
                    2024, 9, 19, 10, 51, 37, 903999, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="professorcontact",
            name="created_at",
            field=django_jalali.db.models.jDateTimeField(
                default=datetime.datetime(
                    2024, 9, 19, 10, 51, 37, 903999, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
