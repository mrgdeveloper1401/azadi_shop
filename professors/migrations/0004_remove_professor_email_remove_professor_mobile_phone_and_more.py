# Generated by Django 5.0.8 on 2024-09-16 07:51

import professors.validators
import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("professors", "0003_alter_professorcontact_contact_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="professor",
            name="email",
        ),
        migrations.RemoveField(
            model_name="professor",
            name="mobile_phone",
        ),
        migrations.AddField(
            model_name="professorcontact",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, null=True, verbose_name="email"
            ),
        ),
        migrations.AddField(
            model_name="professorcontact",
            name="mobile_phone",
            field=models.CharField(
                blank=True,
                max_length=11,
                null=True,
                validators=[users.validators.MobileValidator()],
                verbose_name="mobile phone",
            ),
        ),
        migrations.AlterField(
            model_name="professor",
            name="nation_code",
            field=models.CharField(
                max_length=11,
                unique=True,
                validators=[professors.validators.NationCodeValidator()],
                verbose_name="nation code",
            ),
        ),
    ]