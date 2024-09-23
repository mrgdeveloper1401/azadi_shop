# Generated by Django 5.0.8 on 2024-09-23 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0008_like_dislike_alter_like_course_alter_like_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="course",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True, "is_sale": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_comment",
                to="courses.course",
            ),
        ),
        migrations.AlterField(
            model_name="discountcourse",
            name="course",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True, "is_sale": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_discount",
                to="courses.course",
            ),
        ),
    ]
