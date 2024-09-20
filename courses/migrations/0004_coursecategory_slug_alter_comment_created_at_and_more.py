# Generated by Django 5.0.8 on 2024-09-20 06:30

import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0003_alter_comment_created_at_alter_course_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursecategory",
            name="slug",
            field=models.SlugField(
                allow_unicode=True, blank=True, max_length=200, null=True
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="created_at",
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="course",
            name="created_at",
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
    ]
