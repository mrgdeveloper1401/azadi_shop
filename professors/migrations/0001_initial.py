# Generated by Django 5.0.8 on 2024-09-09 12:07

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Professor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=255, verbose_name="last_name"),
                ),
                (
                    "nation_code",
                    models.CharField(
                        max_length=11, unique=True, verbose_name="nation code"
                    ),
                ),
                (
                    "birth_date",
                    django_jalali.db.models.jDateField(
                        blank=True, null=True, verbose_name="birth date"
                    ),
                ),
                (
                    "field_of_study",
                    models.CharField(max_length=255, verbose_name="field of study"),
                ),
                (
                    "name_of_education",
                    models.CharField(max_length=255, verbose_name="name of education"),
                ),
                (
                    "education_status",
                    models.CharField(
                        choices=[
                            ("دیپلم", "Diploma"),
                            ("فارغ التحصیل کاردانی", "AssociateـGraduate"),
                            ("دانشجوی کارشناسی", "Undergraduate Student"),
                            ("فارغ التحصیل کارشناسی", "Bachelors Student"),
                            ("دانشجوی کارشناسی ارشد", "Master Student"),
                            ("فارغ التحصیل کارشناسی ارشد", "Master Degree Graduate"),
                            ("دانشجوی دکترا", "Doctoral Student"),
                            ("فارغ التحصیل دکترا", "Phd Graduate"),
                        ],
                        max_length=26,
                        verbose_name="education status",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "certificate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="certificate_image",
                        to="images.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "professor",
                "verbose_name_plural": "professors",
                "db_table": "professors",
            },
        ),
    ]