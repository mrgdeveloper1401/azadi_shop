# Generated by Django 5.1.1 on 2024-10-23 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_grade_grade_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="gradegpa",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "نمره کاربر",
                "verbose_name_plural": "نمرات کاربر",
            },
        ),
        migrations.AlterField(
            model_name="gradegpa",
            name="grade",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="grade_gpa",
                to="users.grade",
                verbose_name="پایه",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="gradegpa",
            unique_together={("grade", "gpa")},
        ),
    ]
