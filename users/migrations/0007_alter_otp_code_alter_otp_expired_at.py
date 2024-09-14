# Generated by Django 5.0.8 on 2024-09-14 12:47

import datetime
import users.random_code
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_otp_code_alter_otp_expired_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="otp",
            name="code",
            field=models.PositiveIntegerField(
                default=users.random_code.generate_random_code,
                unique=True,
                verbose_name="OTP code",
            ),
        ),
        migrations.AlterField(
            model_name="otp",
            name="expired_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 9, 14, 12, 49, 29, 794228, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
