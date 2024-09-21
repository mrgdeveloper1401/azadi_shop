# Generated by Django 5.0.8 on 2024-09-21 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_settings", "0002_toprank_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="toprank",
            name="title",
            field=models.CharField(
                choices=[
                    ("experimental", "experimental"),
                    ("math", "math"),
                    ("human", "human"),
                ],
                max_length=12,
                verbose_name="title",
            ),
        ),
    ]
