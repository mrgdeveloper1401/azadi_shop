# Generated by Django 5.0.8 on 2024-09-16 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="course",
            old_name="sales",
            new_name="sale_number",
        ),
        migrations.AddField(
            model_name="course",
            name="is_free",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="coursecategory",
            name="name",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name="discountcourse",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]