# Generated by Django 5.0.8 on 2024-08-28 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_passwordotp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='roll',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
