# Generated by Django 5.0.8 on 2024-09-09 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
        ("professors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="professor",
            name="professor_image",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="professor_image",
                to="images.image",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="professor",
            name="certificate",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="certificate_image",
                to="images.image",
            ),
        ),
        migrations.AlterField(
            model_name="professor",
            name="education_status",
            field=models.CharField(
                choices=[
                    ("دیپلم", "دیپلم"),
                    ("فارغ التحصیل کاردانی", "فارغ التحصیل کاردانی"),
                    ("دانشجوی کارشناسی", "دانشجوی کارشناسی"),
                    ("فارغ التحصیل کارشناسی", "فارغ التحصیل کارشناسی"),
                    ("دانشجوی کارشناسی ارشد", "دانشجوی کارشناسی ارشد"),
                    ("فارغ التحصیل کارشناسی ارشد", "فارغ التحصیل کارشناسی ارشد"),
                    ("دانشجوی دکترا", "دانشجوی دکترا"),
                    ("فارغ التحصیل دکترا", "فارغ التحصیل دکترا"),
                ],
                max_length=26,
                verbose_name="education status",
            ),
        ),
    ]
