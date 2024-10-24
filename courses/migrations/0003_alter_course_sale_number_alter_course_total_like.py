# Generated by Django 5.1.1 on 2024-10-23 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="sale_number",
            field=models.PositiveSmallIntegerField(
                default=0, editable=False, verbose_name="تعداد فروش دوره"
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="total_like",
            field=models.PositiveIntegerField(
                default=0, editable=False, verbose_name="تعداد کاربران پسندیده شده"
            ),
        ),
    ]
