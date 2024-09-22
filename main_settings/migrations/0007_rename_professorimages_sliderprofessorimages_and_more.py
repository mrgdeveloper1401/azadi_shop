# Generated by Django 5.0.8 on 2024-09-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0003_alter_image_created_at"),
        ("main_settings", "0006_alter_footersocial_social_url"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ProfessorImages",
            new_name="SliderProfessorImages",
        ),
        migrations.RenameModel(
            old_name="TopRank",
            new_name="TopRankStudent",
        ),
        migrations.RemoveField(
            model_name="slider",
            name="slider_image",
        ),
        migrations.AddField(
            model_name="slider",
            name="slider_image",
            field=models.ManyToManyField(
                related_name="slider_image", to="images.image"
            ),
        ),
    ]