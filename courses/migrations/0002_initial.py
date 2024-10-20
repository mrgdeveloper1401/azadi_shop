# Generated by Django 5.1.1 on 2024-10-19 20:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("courses", "0001_initial"),
        ("images", "0001_initial"),
        ("professors", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True, "is_verified": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_comment",
                to=settings.AUTH_USER_MODEL,
                verbose_name="کاربر",
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="course_image",
                to="images.image",
                verbose_name="عکس دوره",
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="professor",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="professor_course",
                to="professors.professor",
                verbose_name="استاد",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="course",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True, "is_sale": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_comment",
                to="courses.course",
                verbose_name="دوره",
            ),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="icon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="image_category",
                to="images.image",
                verbose_name="عکس دسته بندی",
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="category",
            field=models.ManyToManyField(
                related_name="category_course",
                to="courses.coursecategory",
                verbose_name="دسته بندی",
            ),
        ),
        migrations.AddField(
            model_name="discountcourse",
            name="course",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True, "is_free": False, "is_sale": True},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="course_discount",
                to="courses.course",
                verbose_name="دوره",
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="course",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="course_like",
                to="courses.course",
                verbose_name="دوره",
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True, "is_verified": True},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="user_like",
                to=settings.AUTH_USER_MODEL,
                verbose_name="کاربر",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="like",
            unique_together={("user", "course")},
        ),
    ]
