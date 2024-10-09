# Generated by Django 5.1.1 on 2024-10-09 10:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("images", "0003_alter_image_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("path", models.CharField(max_length=255, unique=True)),
                ("depth", models.PositiveIntegerField()),
                ("numchild", models.PositiveIntegerField(default=0)),
                ("category_name", models.CharField(max_length=50, unique=True)),
                ("category_slug", models.SlugField(allow_unicode=True, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BlogPostImage",
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
                ("is_active", models.BooleanField(default=True)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="fk_blog_post_image",
                        to="images.image",
                    ),
                ),
            ],
            options={
                "verbose_name": "'Blog Post Image'",
                "verbose_name_plural": "Blog Post Images",
                "db_table": "blog_post_images",
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
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("post_title", models.CharField(max_length=255, unique=True)),
                (
                    "slug",
                    models.SlugField(allow_unicode=True, max_length=255, unique=True),
                ),
                ("post_body", models.TextField()),
                ("is_publish", models.BooleanField(default=False)),
                ("view_number", models.PositiveIntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="user_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(
                        related_name="posts", to="blogs.categorynode"
                    ),
                ),
                (
                    "post_image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="post_images",
                        to="blogs.blogpostimage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
                "db_table": "posts",
            },
        ),
        migrations.AddField(
            model_name="blogpostimage",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="fk_blog_post",
                to="blogs.post",
            ),
        ),
    ]
