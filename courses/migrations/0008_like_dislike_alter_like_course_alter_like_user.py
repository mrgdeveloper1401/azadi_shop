# Generated by Django 5.0.8 on 2024-09-21 14:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0007_course_total_like_like"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="like",
            name="dislike",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="like",
            name="course",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="course_like",
                to="courses.course",
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True, "is_verified": True},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="user_like",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]