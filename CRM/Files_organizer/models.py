from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class ProgrammingPath(models.Model):
    name = models.CharField(max_length=50)
    logo_image = models.ImageField(upload_to="path_images")
    path_image = models.ImageField(upload_to="path_images")
    about = models.TextField()
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Subject(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    programming_path = models.ForeignKey(ProgrammingPath, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        index = self.name.find("_")
        if index > -1:
            self.slug = slugify(self.name[:index])
        else:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Topic(models.Model):
    user = models.ManyToManyField(User)
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Document(models.Model):
    class Type(models.TextChoices):
        THEORY = "THEORY"
        EXERCISE = "EXERCISE"
        EXTRA = "EXTRA"

    file = models.FileField(upload_to="files")
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=Type.choices)

    def __str__(self):
        return self.name
