# Generated by Django 5.0.8 on 2024-09-14 12:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_userinfo_deleted_at_userinfo_is_deleted_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userinfo",
            name="deleted_at",
        ),
        migrations.RemoveField(
            model_name="userinfo",
            name="is_deleted",
        ),
        migrations.AlterField(
            model_name="otp",
            name="expired_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 9, 14, 12, 2, 18, 20433, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
