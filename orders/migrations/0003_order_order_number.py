# Generated by Django 5.0.8 on 2024-09-26 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_number",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="order number"
            ),
        ),
    ]