# Generated by Django 5.0.8 on 2024-10-01 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0002_alter_image_created_at_alter_image_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="file_hash",
            field=models.CharField(blank=True, max_length=40, null=True, unique=True),
        ),
    ]