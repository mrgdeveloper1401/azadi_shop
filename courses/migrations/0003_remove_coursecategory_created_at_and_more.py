# Generated by Django 5.0.8 on 2024-09-09 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="coursecategory",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="coursecategory",
            name="parent",
        ),
        migrations.RemoveField(
            model_name="coursecategory",
            name="updated_at",
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="depth",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="numchild",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="path",
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="coursecategory",
            name="name",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
