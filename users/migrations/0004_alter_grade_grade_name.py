# Generated by Django 5.1.1 on 2024-10-23 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_gradegpa_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grade",
            name="grade_name",
            field=models.CharField(max_length=20, verbose_name="نام پایه"),
        ),
    ]
