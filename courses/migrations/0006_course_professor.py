# Generated by Django 5.0.8 on 2024-09-09 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0005_remove_course_user"),
        ("professors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="professor",
            field=models.ForeignKey(
                default=0,
                limit_choices_to={"is_active": True},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="professor_course",
                to="professors.professor",
            ),
            preserve_default=False,
        ),
    ]