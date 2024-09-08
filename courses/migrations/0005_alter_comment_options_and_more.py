# Generated by Django 5.0.8 on 2024-09-08 15:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0004_rename_desc_course_description"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"verbose_name": "comment", "verbose_name_plural": "comments"},
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="updated",
            new_name="updated_at",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="admin_response",
        ),
        migrations.AlterField(
            model_name="comment",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_comment",
                to="courses.course",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="public",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelTable(
            name="comment",
            table="comment",
        ),
    ]
