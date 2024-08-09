from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    """
    This model describes subject
    """
    title = models.CharField(
        "Название",
        max_length=250,
    )
    slug = models.SlugField(
        "Слаг",
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Course(models.Model):
    """
    This model describes course
    """
    title = models.CharField(
        "Название",
        max_length=250,
    )
    slug = models.SlugField(
        "Слаг",
        max_length=250,
        unique=True,
    )
    description = models.TextField(
        "Описание",
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        related_name="course_created",
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
