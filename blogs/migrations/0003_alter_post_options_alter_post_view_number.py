# Generated by Django 5.1.1 on 2024-10-23 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={
                "verbose_name": "پست وبلاگ",
                "verbose_name_plural": "پست های وبلاگ",
            },
        ),
        migrations.AlterField(
            model_name="post",
            name="view_number",
            field=models.PositiveIntegerField(
                default=0, editable=False, verbose_name="تعداد بازدید"
            ),
        ),
    ]