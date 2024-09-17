# Generated by Django 5.0.8 on 2024-09-16 07:25

import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("professors", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="professor",
            name="mobile_phone",
            field=models.CharField(
                blank=True,
                max_length=11,
                null=True,
                validators=[users.validators.MobileValidator()],
                verbose_name="mobile phone",
            ),
        ),
    ]