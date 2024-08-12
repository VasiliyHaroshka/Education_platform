from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .fields import OrderField


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


class Module(models.Model):
    """
    This model describes module
    """
    title = models.CharField(
        "Название",
        max_length=250,
    )
    description = models.TextField(
        "Описание",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name="Курс",
    )
    order = OrderField(
        "Порядок",
        blank=True,
        for_fields=["course"],  # порядок вычисляется относительно курса
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"


class Content(models.Model):
    """
    This model describes different types of content
    """
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="content",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": (
                "text",
                "file",
                "image",
                "video",
            )
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey(
        "content_type",
        "object_id",
    )


class ItemBase(models.Model):
    """
    Abstract model which gives features to different types of content, that inherit from it
    """
    title = models.CharField(
        "Название",
        max_length=250,
    )
    created_at = models.DateTimeField(
        "Создано",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Изменено",
        auto_now=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_related"
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    content = models.FileField(upload_to="files")


class Image(ItemBase):
    content = models.FileField(upload_to="images")


class Video(ItemBase):
    content = models.URLField()
