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
