# Generated by Django 5.1.1 on 2024-10-19 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CategoryNode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("path", models.CharField(max_length=255, unique=True)),
                ("depth", models.PositiveIntegerField()),
                ("numchild", models.PositiveIntegerField(default=0)),
                (
                    "category_name",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="نام دسته بندی"
                    ),
                ),
                (
                    "category_slug",
                    models.SlugField(
                        allow_unicode=True, unique=True, verbose_name="اسلاگ دسته بندی"
                    ),
                ),
            ],
            options={
                "verbose_name": "دسته بندی",
                "verbose_name_plural": "دسته بندی ها",
                "db_table": "blog_category",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "post_title",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="عنوان پست"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        max_length=255,
                        unique=True,
                        verbose_name="اسلاگ",
                    ),
                ),
                ("post_body", models.TextField(verbose_name="متن پست")),
                (
                    "is_publish",
                    models.BooleanField(default=False, verbose_name="قابل انتشار"),
                ),
                (
                    "view_number",
                    models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید"),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
                "db_table": "blog_post",
            },
        ),
    ]
