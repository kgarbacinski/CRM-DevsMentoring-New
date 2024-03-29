# Generated by Django 4.0.3 on 2022-03-30 17:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgrammingPath",
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
                ("name", models.CharField(max_length=50)),
                ("logo_image", models.ImageField(upload_to="path_images")),
                ("path_image", models.ImageField(upload_to="path_images")),
                ("about", models.TextField()),
                ("slug", models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField()),
                (
                    "programming_path",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Files_organizer.programmingpath",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubTopic",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField()),
                ("description", models.TextField()),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Files_organizer.subject",
                    ),
                ),
                ("user", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Document",
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
                ("file", models.FileField(upload_to="files")),
                ("name", models.CharField(max_length=50)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("THEORY", "Theory"),
                            ("EXERCISE", "Exercise"),
                            ("EXTRA", "Extra"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "subtopic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Files_organizer.subtopic",
                    ),
                ),
            ],
        ),
    ]
