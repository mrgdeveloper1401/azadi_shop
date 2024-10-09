# Generated by Django 5.1.1 on 2024-10-09 10:14

import images.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0002_image_image_base64"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(
                height_field="height",
                help_text="max size is 5 MG",
                upload_to="images/%Y/%m/%d",
                validators=[images.validators.validate_image_size],
                width_field="width",
            ),
        ),
    ]
