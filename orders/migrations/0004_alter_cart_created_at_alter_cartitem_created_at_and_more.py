# Generated by Django 5.0.8 on 2024-09-20 06:30

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_alter_cart_created_at_alter_cartitem_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="created_at",
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="created_at",
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="created_at",
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
    ]
